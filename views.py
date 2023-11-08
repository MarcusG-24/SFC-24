from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user

from sqlalchemy import create_engine

from .models import Entries, Note, Students,  Houses, Activities
from . import db
import json
import sqlite3

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    # using SQL alchemy to collect all of the information for activities 
    activities=Activities.query.order_by(Activities.act_Code).all()
    count=Activities.query.count()
    return render_template("home.html", count=count, activities=activities, user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


# This next set of Functions is for Managing activities
# ---------------------------------------------------------------------------------

# This function is used to show Gala Day Activities from the Activities table
@views.route('/activities', methods=['GET'])
@login_required
def activities():
     # loads all activities
         # using flask message to confirm activity read
    flash('Read Activities !', category='success')
    activities=Activities.query.order_by(Activities.act_Code).all()
    # counts all activities using the two filters of grade / Gender
    count=Activities.query.count()
    return render_template("activities.html",
                            activities=activities,
                            count=count,
                            user =current_user)

# This function is used to show Gala Day Activities from the Activities table
@views.route('/updateAct', methods=['GET'])
@login_required
def updateActivity():
      # using flask message to confirm activity update options
    flash('Update Activity !', category='success')
    activities=Activities.query.order_by(Activities.act_Code).all()
    count=Activities.query.count()
    return render_template("update.html",
                            activities=activities,
                            count=count,
                            user =current_user)

# loads a url using update/activity - used as link as POST to update activity details
@views.route('/update/<act_Code>', methods=['GET', 'POST'])
def update(act_Code):
    # sqlalchemy query to get activity details
    activity = Activities.query.get_or_404(act_Code)
    # if POST method used to collect new information and update details 
    if request.method == 'POST':
        # existing details loaded into activitys table from request form
        activity.act_Code = request.form['code']
        activity.act_Name = request.form['name']
        activity.min = request.form['min']
        
         # updated activity added to activity table using db session using commit
        try:    
            db.session.commit()
            # using flask message to confirm activity update
            flash('Activity updated!   :o)', category='success')
            # sql alchemy query to get latest list of activity details
            activities = Activities.query.order_by(Activities.act_Code).all()
            count=Activities.query.count()
            return render_template("updateAct.html",
                                   user=current_user,
                                   count=count,
                                   activity=activity,
                                   activities=activities,
                                   user_id=current_user.id)
        except:
            # error feedback for coding debugging
            return 'There was an issue updating your Activity'

    else:
        # using flask message to show activity update possibility
        flash('Update Activity !', category='warning')
        activities = Activities.query.order_by(Activities.act_Code).all()
        count=Activities.query.count()
        return render_template('updateAct.html',
                               count=count, 
                               activity=activity,
                               user=current_user,
                               activities=activities)

# Create new Activity loads a url using /addAct - used as link as POST to add a new activity via addAct.html
@views.route('/addAct', methods=['GET', 'POST'])
def add():
    # if POST method used to collect new information added details 
    if request.method == 'POST':
        # existing details loaded into activity table from request form
        act_Code = request.form['code']
        act_Name = request.form['name']
        min = request.form['min']
        
         # updated activity added to activity table using db session using add and commit
        try:
            new_activity = Activities(act_Code=act_Code,act_Name=act_Name,min=min)
            db.session.add(new_activity)  
            db.session.commit()
            # using flask message to confirm activity added
            flash('Activity added!', category='success')
            # sql alchemy query to get latest list of activity details
            
            activities = Activities.query.order_by(Activities.act_Code).all()
            count=Activities.query.count()
            return render_template("addAct.html",
                                   user=current_user,
                                   count=count,
                                   activities=activities,
                                   user_id=current_user.id)
        except:
            # error feedback for coding debugging
            return 'There was an issue adding your Activity'

    else:
        # using flask message to show activity update possibility
        flash('Creating Activity !', category='success')
        
        activities = Activities.query.order_by(Activities.act_Code).all()
        count=Activities.query.count()
        return render_template('addAct.html',
                               user=current_user,
                               count=count,
                               activities=activities)

# loads a url using delete/<act_Code> - used as link as POST to delete activity details
@views.route('/delete/<act_Code>', methods=['GET', 'POST'])
def delete(act_Code):
    # sqlalchemy query to get activity details
    
    activities = Activities.query.order_by(Activities.act_Code).all()
    delActivity = Activities.query.get_or_404(act_Code)
    act_Name = delActivity.act_Name
    count=Activities.query.count()
    return render_template("delAct.html",
                               user=current_user,
                               act_Name=act_Name,
                               count=count,
                               activities=activities,
                               user_id=current_user.id,
                               act_Code = act_Code,)


# loads a url using delete/<act_Code> - used as link as POST to delete activity details
@views.route('/deleteConfirm/<act_Code>', methods=['GET', 'POST'])
def deleteConfirm(act_Code):
    # sqlalchemy query to get activity details
    
   
    delActivity = Activities.query.get_or_404(act_Code)
    
        # deleting activity from table using db session using delete and commit
    try:    
        db.session.delete(delActivity)
        db.session.commit()
        # using flask message to confirm activity deleted
        flash('Activity deleted!', category='success')
        # sql alchemy query to get latest list of activity details
        activities = Activities.query.order_by(Activities.act_Code).all()
        count=Activities.query.count()
        
        return render_template("delAct.html",
                               user=current_user,
                               count=count,
                               activities=activities,
                               user_id=current_user.id)
    except:
        # error feedback for coding debugging
        return 'There was an issue deleting your Activity'

    # loads a url using /delAct - used as link as POST to delete Activity details
@views.route('/delAct', methods=['GET', 'POST'])

def delAct():
    # using flask message to show activity delete options
    flash('Delete Activity !', category='success')
    # sqlalchemy query to get activity details
    activities = Activities.query.order_by(Activities.act_Code).all()
    count=Activities.query.count()
    return render_template('delAct.html', 
                           user=current_user,
                           count=count,
                           activities=activities)

    # end of Functions to Manage Activities
    #  ---------------------------------------------------------------------------------

# This next set of Functions is to  manage Student lists by Gender, Team and or Grade
#  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# This function is used to enable the URL  /students  to show all students in a student.html file
@views.route('/students', methods=['GET'])
@login_required
def students():
     # loads all students
    
    students=Students.query.all()
    count=Students.query.count()
    return render_template("students.html",
                            students=students,
                            count=count,
                            user =current_user)

# This function is used to enable the URL  /students/<gender> to show students by gender in a student.html file
@views.route('/students/<gender>', methods=['GET'])
@login_required
def gender(gender):
     # loads all students using the filter of Gender
    students=Students.query.filter_by(gender=gender).order_by(Students.surname).all()
    count=Students.query.filter_by(gender=gender).count()
    return render_template("students.html", 
                                students=students,
                                gender=gender,
                                count=count,
                                user =current_user)


# This function is used to show students in /student/team/<team> in a student table
@views.route('/students/team/<team>', methods=['GET'])
@login_required
def teams(team):
     # loads all students using the one filter of Team
    students=Students.query.filter_by(team=team).order_by(Students.surname).all()
    count=Students.query.filter_by(team=team).count()
    
    # loads all house info ( colors house name etc) for current team
    houseInfo=Houses.query.filter_by(team=team).one()
    # identifies current house name
    housename=houseInfo.house
    # identifies current house color
    bgcolor=houseInfo.bgcolor

    return render_template("students.html",
                                students=students,
                                count=count,
                                team=team,
                                bgcolor=bgcolor,
                                house=housename,
                                user =current_user)


# This function is used to show students in <teams> AND <gender> in a student table
@views.route('/students/<team>/<grade>', methods=['GET'])
@login_required
def teamsGrade(team,grade):
     # loads all students using the two filters of Team / gender
    students=Students.query.filter_by(team=team).filter_by(grade=grade).order_by(Students.surname).all()
    count=Students.query.filter_by(team=team).filter_by(grade=grade).count()
    
    # loads all house info ( colors house name etc) for current team
    houseInfo=Houses.query.filter_by(team=team).one()
    # identifies current house name
    housename=houseInfo.house
    # identifies current house colour
    bgcolor=houseInfo.bgcolor

    return render_template("students.html",
                                students=students,
                                count=count,
                                team=team,
                                bgcolor=bgcolor,
                                house=housename,
                                user =current_user)



# This function is used to show students in <grade> AND <gender> in a student table
@views.route('/students/<grade><gender>', methods=['GET'])
@login_required
def gradeGender(grade,gender):
     # loads all students using the two filters of grade / Gender
    students=Students.query.filter_by(grade=grade).filter_by(gender=gender).order_by(Students.surname).all()
    # counts all students using the two filters of grade / Gender
    count=Students.query.filter_by(grade=grade).filter_by(gender=gender).count()

    return render_template("students.html",
                                students=students,
                                count=count,
                                grade=grade,
                                gender=gender,
                                user =current_user)
    
    
# This function is used to show students in <teams> AND <grade> AND <gender> in a student table
@views.route('/students/<team>/<grade><gender>', methods=['GET'])
@login_required
def teamsGradeGender(team,grade,gender):
     # loads all students using the three filters of Team / grade / Gender
    students=Students.query.filter_by(team=team).filter_by(grade=grade).filter_by(gender=gender).order_by(Students.surname).all()
    count=Students.query.filter_by(team=team).filter_by(grade=grade).filter_by(gender=gender).count()
    
    # loads all house info ( colors house name etc) for current team
    houseInfo=Houses.query.filter_by(team=team).one()
    # identifies current house name
    housename=houseInfo.house
    # identifies current house color
    bgcolor=houseInfo.bgcolor

    return render_template("students.html",
                                students=students,
                                count=count,
                                team=team,
                                grade=grade,
                                gender=gender,
                                bgcolor=bgcolor,
                                house=housename,
                                user =current_user)
    
# End of Functions Managing the Student reports
#  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# next set of Functions are used to manage Activities for students
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    # loads a url using /entries/<team>/<grade><gender> 
    # # used as link with POST method to add a new entry into entries table
@views.route('/entries/<team>/<grade><gender>', methods=['GET', 'POST'])
def entries(team,grade,gender):
    
    # if POST method used to collect new entry information to add details 
    activities = Activities.query.order_by(Activities.act_Code).all()
    students = Students.query.filter_by(team=team).filter_by(grade=grade).filter_by(gender=gender).order_by(Students.surname).all()
    count = Students.query.filter_by(team=team).filter_by(grade=grade).filter_by(gender=gender).count()
    entries = Entries.query.filter_by(team=team).filter_by(grade=grade).filter_by(gender=gender).order_by(Entries.surname).all()
    ecount = Entries.query.filter_by(team=team).filter_by(grade=grade).filter_by(gender=gender).count()
    team=(team)
    grade=(grade)
    gender=(gender)
    houseInfo=Houses.query.filter_by(team=team).one()
    # identifies current house name
    house=houseInfo.house
    # identifies current house colour
    bgcolor=houseInfo.bgcolor
    if request.method == 'POST':
        # existing details loaded into activity table from request form
        act_Code = request.form['act_Code']
        activityinfo = Activities.query.get_or_404(act_Code)
        act_Name = activityinfo.act_Name
        studID = request.form['studID']
        studentInfo = Students.query.get_or_404(studID)
        name=studentInfo.name
        surname=studentInfo.surname
        team=studentInfo.team
      
         # updated activity added to activity table using db session using add and commit
        try:
            newEntry = Entries(studID=studID,
                               act_Code=act_Code,
                               act_Name=act_Name,
                               name=name,
                               surname=surname,
                               team=team,
                               grade=grade,
                               gender=gender,
                               
                               )
            db.session.add(newEntry)  
            db.session.commit()
            # using flask message to confirm activity added
            flash('Entry added!', category='success')
            activities = Activities.query.order_by(Activities.act_Code).all()
            students = Students.query.filter_by(team=team).filter_by(grade=grade).filter_by(gender=gender).order_by(Students.surname).all()
            count = Students.query.filter_by(team=team).filter_by(grade=grade).filter_by(gender=gender).count()
            entries = Entries.query.filter_by(team=team).filter_by(grade=grade).filter_by(gender=gender).order_by(Entries.surname).all()
            ecount = Entries.query.filter_by(team=team).filter_by(grade=grade).filter_by(gender=gender).count()
            # sql alchemy query to get latest list of activity details
            
            return render_template("entries.html",
                                    user=current_user,
                                    activities=activities,
                                    students=students,
                                    count=count,
                                    entries=entries,
                                    ecount=ecount,
                                    team=team,
                                    house=house,
                                    bgcolor=bgcolor,
                                    grade=grade,
                                    gender=gender,
                                    user_id=current_user.id)
        except:
            # error feedback for coding debugging
            return 'There was an issue adding your Entry.  Please try again'

    else:
        # using flask message to show activity update possibility
        flash('Students Gala Day Entries !', category='success')
        
       
        return render_template('entries.html',user=current_user,
                                    activities=activities,
                                    students=students,
                                    count=count,
                                    entries=entries,
                                    ecount=ecount,
                                    team=team,
                                    house=house,
                                    bgcolor=bgcolor,
                                    grade=grade,
                                    gender=gender,
                                    user_id=current_user.id)



    # loads a url using /addEntry - used as link as POST to add a new entry into activity
@views.route('/delete/<int:entryID>', methods=['GET', 'POST'])
def delEntry(entryID):
    entryInfo=Entries.query.get_or_404(entryID)
    team=entryInfo.team
    grade=entryInfo.grade
    gender=entryInfo.gender
    houseInfo=Houses.query.filter_by(team=team).one()
    # identifies current house name
    house=houseInfo.house
    # identifies current house colour
    bgcolor=houseInfo.bgcolor
    # if POST method used to collect new entry information to add details 
    activities = Activities.query.order_by(Activities.act_Code).all()
    students = Students.query.filter_by(team=team).filter_by(grade=grade).filter_by(gender=gender).order_by(Students.surname).all()
    count = Students.query.filter_by(team=team).filter_by(grade=grade).filter_by(gender=gender).count()
    entries = Entries.query.filter_by(team=team).filter_by(grade=grade).filter_by(gender=gender).order_by(Entries.surname).all()
    ecount = Entries.query.filter_by(team=team).filter_by(grade=grade).filter_by(gender=gender).count()
    team=(team)
    grade=(grade)
    gender=(gender)
    if request.method == 'POST':
        # existing details loaded into activity table from request form
        entryID = request.form['entryID']
        delEntry = Entries.query.get_or_404(entryID)
    
        # deleting activity from table using db session using delete and commit
        try:    
            db.session.delete(delEntry)
            db.session.commit()
            # using flask message to confirm activity added
            flash('Entry deleted!', category='success')
            activities = Activities.query.order_by(Activities.act_Code).all()
            students = Students.query.filter_by(team=team).filter_by(grade=grade).filter_by(gender=gender).order_by(Students.surname).all()
            count = Students.query.filter_by(team=team).filter_by(grade=grade).filter_by(gender=gender).count()
            entries = Entries.query.filter_by(team=team).filter_by(grade=grade).filter_by(gender=gender).order_by(Entries.surname).all()
            ecount = Entries.query.filter_by(team=team).filter_by(grade=grade).filter_by(gender=gender).count()
            # sql alchemy query to get latest list of activity details
            
            return render_template("entries.html",
                                    user=current_user,
                                    students=students,
                                    count=count,
                                    team=team,
                                    house=house,
                                    bgcolor=bgcolor,
                                    grade=grade,
                                    gender=gender,
                                    activities=activities,
                                    entries=entries,
                                    ecount=ecount,
                                    user_id=current_user.id)
        except:
            # error feedback for coding debugging
            return 'There was an issue adding your Entry.  Please try again'

        else:
            # using flask message to show activity update possibility
            flash('Read Entries !', category='success')
        
        
    return render_template('entries.html',
                        user=current_user,
                        students=students,
                        team=team,
                        grade=grade,
                        gender=gender,
                        activities=activities,
                        entries=entries,
                        ecount=ecount,
                        user_id=current_user.id)

#  end of Functions for managing Activities for Students
#  &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

#  Start of Functions for managing Reports of Students by Team and Activity 
#  &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

   # loads a url /report/<team> - used to show a report of the teams entries
@views.route('/report/<team>', methods=['GET'])
def teamActivities(team):
     # loads team from Parameter as variable for use in this function
    team=(team)
    # sqlalchemy used to SELECT * FROM Activities ORDER BY act_code 
    activities = Activities.query.order_by(Activities.act_Code).all()
    # sqlalchemy used to SELECT COUNT FROM Students WHERE team =<team>
    count = Students.query.filter_by(team=team).count()
    # sqlalchemy used to SELECT * FROM entries WHERE team =<team>  ORDER BY act_Code
    entries = Entries.query.filter_by(team=team).order_by(Entries.act_Code).all()
    # sqlalchemy used to SELECT COUNT FROM Entries WHERE team =<team>
    ecount = Entries.query.filter_by(team=team).count()
  
    houseInfo=Houses.query.filter_by(team=team).one()
    # identifies current house name
    house=houseInfo.house
    # identifies current house colour
    bgcolor=houseInfo.bgcolor

    # using flask message to show activity update possibility
    flash('Check House Entries into Activities !', category='success')

    # send info below to the report.html page for use in the {{Jinja2 Data}} components
    return render_template('report.html',
                            user=current_user,
                            team=team,
                            house=house,
                            bgcolor=bgcolor,
                            activities=activities,
                            entries=entries,
                            ecount=ecount,
                            count=count,
                            user_id=current_user.id)


 # loads a url /team/<act_Code> - used to show a report of the activity entries
@views.route('/team/<act_Code>', methods=['GET'])
def teamActivity(act_Code):
    # loads act_Code from Parameter as variable for use in this function
    act_Code=act_Code
     # uses act_Code in SQLAlchemy to SELECT * From Activities WHERE act_Code = <act_Code>
    activityInfo = Activities.query.get_or_404(act_Code)
    # assigns the act_Name using SQLALchemy to get Activity Name using
    # SELECT act_Name FROM Activities WHERE act_Code = <act_Code>
    act_Name = activityInfo.act_Name
     # sqlalchemy used to SELECT * FROM Activities ORDER BY act_code 
    activities = Activities.query.order_by(Activities.act_Code).all()
    # sqlalchemy used to SELECT * FROM Houses 
    teams=Houses.query.order_by(Houses.team).all()
    # sqlalchemy used to SELECT * FROM entries WHERE team =<team>  ORDER BY act_Code
    entries = Entries.query.filter_by(act_Code=act_Code).order_by(Entries.act_Code).all()
     # sqlalchemy used to SELECT COUNT FROM Entries WHERE act_Code = <act_Code>
    a_count = Entries.query.filter_by(act_Code=act_Code).count()
    
    # using flask message to show activity house teams
    flash('Activity House Teams Revealed!', category='success')
     # send info below to the activityTeams.html page for use in the {{Jinja2 Data}} components
    return render_template('activityTeams.html',
                            user=current_user,
                            teams=teams,
                            activity=activityInfo,
                            activities=activities,
                            act_Name=act_Name,
                            entries=entries,
                            a_count=a_count,
                            user_id=current_user.id)



