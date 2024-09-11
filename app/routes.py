import flask
from flask import send_file, redirect, url_for
from datetime import datetime
from app import app
from app.forms import LoginForm, SessionForm, StudentSignInForm, AddUnitForm
from app.helpers import get_perth_time
from app.utilities import process_csv, export_all_to_zip
from app.models import User
import sqlalchemy as sa
from app import database
from flask_login import current_user, login_user, logout_user, login_required
import os

# HOME -   /home/
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
@login_required
def home():
    form = StudentSignInForm()    
    #placeholder data for table
    students = []
    alex = {
        "name": "alex",
        "id": "12345678",
        "login": "yes",
        "photo": "yes"
    }
    bob = {
        "name": "bob",
        "id": "87654321",
        "login": "no",
        "photo": "yes"
    }
    cathy = {
        "name": "cathy",
        "id": "22224444",
        "login": "yes",
        "photo": "no"
    }
    
    students.append(alex)
    students.append(bob)
    students.append(cathy)
    return flask.render_template('home.html', form=form, students=students)
	
# CONFIGURATION - /session/ /admin/
@app.route('/session', methods=['GET', 'POST'])
@login_required
def session():    
    form = SessionForm()
    # Get perth time
    perth_time = get_perth_time()
    humanreadable_perth_time = perth_time.strftime('%B %d, %Y, %H:%M:%S %Z')

    # For JS formatting
    formatted_perth_time = perth_time.isoformat()

    if form.validate_on_submit():
        # Handle form submission
        session_name = form.session_name.data
        unit_code = form.unit_code.data
        current_year = perth_time.year

        # Determine the semester based on the current month
        current_month = perth_time.month
        semester = "SEM1" if current_month <= 6 else "SEM2"
        # Create Database
        database_name = f"{unit_code}_{semester}_{current_year}"

        # Printing for debugging
        print(f"Session Name: {session_name}")
        print(f"Unit Code: {unit_code}")
        print(f"Semester: {semester}")
        print(f"Database Name: {database_name}")
        print(f"Current Date/Time: {humanreadable_perth_time}")
        # Redirect back to home page when done
	    
        return flask.redirect(flask.url_for('home'))

    return flask.render_template('session.html', form=form, perth_time=formatted_perth_time)

#ADMIM - /admin/
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.userType != 1:
        return flask.redirect('home')
    # I (James) do not know what to add here so for now it is blank


    return flask.render_template('admin.html')

# ADDUNIT - /addunit/ /admin/
@app.route('/addunit', methods=['GET', 'POST'])
def addunit():
    form = AddUnitForm()
    if form.validate_on_submit():
        #Form data held here
        newunit_code = form.unitcode.data
        semester = form.semester.data
        consent_required = form.consentcheck.data
        student_file = form.studentfile.data
        facilitator_file = form.facilitatorfile.data
        sessionname = form.sessionnames.data
        sessionoccurence = form.sessionoccurence.data
        assessmentcheck = form.assessmentcheck.data
        commentsenabled = form.commentsenabled.data
        commentsuggestions = form.commentsuggestions.data

        #something here to save the csv files somewhere

        #something here to upload csv fiels to database using utilities.py

        #Printing for Debugging
        print(f"Unit Code: {newunit_code}")
        print(f"Semester: {semester}")
        print(f"Consent: {consent_required}")
        print(f"Session Names: {sessionname}")
        print(f"Occurences: {sessionoccurence}")
        print(f"Assessment Check: {assessmentcheck}")
        print(f"Comments Check: {commentsenabled}")
        print(f"Suggestions: {commentsuggestions}")
        
        return flask.redirect(flask.url_for('admin'))
	    
    return flask.render_template('addunit.html', form=form)

@app.route('/export', methods=['GET'])
@login_required
def export_data():
    print("Attempting to Export Database...")
    zip_filename = 'database.zip'

    # Get database.zip filepath
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    zip_path = os.path.join(project_root, zip_filename)

    # Call the function to export all data to the 'database.zip'
    export_all_to_zip(zip_filename)

    # Check if the file was created successfully
    if os.path.exists(zip_path):
        # Serve the zip file for download
        response = send_file(zip_path, as_attachment=True)
        os.remove(zip_path)
        print("Admin Successfully Exported Database")
        return response

    else:
        # Handle the error if the zip file doesn't exist
        return "Error: Could not export the data.", 500


# STUDENT - /student/
@app.route('/student', methods=['GET'])
def student():
    alex = {
        "name": "alex",
        "id": "12345678",
        "login": "yes",
        "photo": "no"
    }
    return flask.render_template('student.html', student=alex)
	
# LOGIN - /login/ 
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        print("authenitcated")
        return flask.redirect('home')
    
    form = LoginForm()
    if form.validate_on_submit():
        user = database.GetUser(uwaID = form.username.data)                

        if user is None or not database.CheckPassword(form.username.data, form.password.data):
            flask.flash('Invalid username or password')
            return flask.redirect('login')
        
        login_user(user, remember=form.remember_me.data)
        return flask.redirect('home')

    return flask.render_template('login.html', form=form)

@app.route('/save_changes', methods=['POST'])
def save_changes():
    # Access form data 
    grade = flask.request.form.get('grade')
    comment = flask.request.form.get('comment')
    photo = flask.request.form.get('photo')

    # Process form data here (save changes to db)

    return flask.redirect('home') 

@app.route('/add_student', methods=['POST'])
def add_student():
    form = StudentSignInForm()

    if form.validate_on_submit():
        # Handle form submission
        student_name = form.student_sign_in.data
        consent_status = form.consent_status.data

        # Printing for debugging
        print(f"Student Name: {student_name}")
        print(f"Consent Status: {consent_status}")

        # Update student info in database (login/consent)

        # Redirect back to home page when done
        return flask.redirect(flask.url_for('home'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return flask.redirect(flask.url_for('login'))
