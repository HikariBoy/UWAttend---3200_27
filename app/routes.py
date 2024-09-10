import flask
from datetime import datetime

from app import app
from .forms import LoginForm, SessionForm, StudentSignInForm
from .utilities import get_perth_time
from .models import db, Student, Session, Attendance
from .database import GetStudent, AddAttendance, GetSession, GetAttendance

# HOME -   /home/
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    form = StudentSignInForm()

    # will need to be replaced with actual session logic later 
    current_session = GetSession(sessionID=1)[0]

    # get students who have signed in for this session
    # attendance_records = db.session.query(Attendance).filter_by(sessionID=current_session.sessionID).all()
    attendance_records = GetAttendance(input_sessionID=current_session.sessionID)

    # get student IDs from the attendance records
    logged_in_student_ids = [str(record.studentID) for record in attendance_records]

    # get only the students who have logged in
    students = db.session.query(Student).filter(Student.studentID.in_(logged_in_student_ids)).all()

    student_list = []
    signed_in_count = 0

    for student in students:
        
        # find the student's attendance record 
        attendance_record = next((record for record in attendance_records if record.studentID == student.studentID), None)

        # set login status based on whether the student has a time marked where they logged out
        login_status = "no" if attendance_record.signOutTime else "yes"

        signed_in_count = signed_in_count + 1 if login_status == "yes" else signed_in_count

        student_info = {
            "name": f"{student.preferredName} {student.lastName}",
            "number": student.studentNumber,
            "id": student.studentID,
            "login": login_status,  
            "photo": "yes" if student.consent == 1 else "no",
            "time": attendance_record.signInTime
        }
        student_list.append(student_info)

    student_list.sort(key=lambda x: x['time'], reverse=True)

    return flask.render_template('home.html', form=form, students=student_list, session=current_session, total_students=len(student_list), signed_in=signed_in_count, session_num=1)
	
# CONFIGURATION - /session/ /admin/
@app.route('/session', methods=['GET', 'POST'])
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

@app.route('/admin', methods=['GET'])
def admin():
    return flask.render_template('admin.html')

# STUDENT - /student/
@app.route('/student', methods=['POST'])
def student():
    student_id = flask.request.form['student_id']

    student = GetStudent(studentID=student_id)[0]

    # will need to be replaced with actual session logic later
    current_session = GetSession(sessionID=1)[0]

    attendance_record = GetAttendance(input_sessionID=current_session.sessionID, studentID=student_id)[0]

    login_status = "no" if attendance_record.signOutTime else "yes"

    if not student:
        flask.flash("Error - Student not found")
        return flask.redirect(flask.url_for('home'))
    
    student_info = {
        "name": f"{student.preferredName} {student.lastName}",
        "number": student.studentNumber,
        "id": student.studentID,
        "login": login_status,  
        "photo": "yes" if student.consent == 1 else "no",
        "time": attendance_record.signInTime
    }

    return flask.render_template('student.html', student=student_info)
	
# LOGIN - /login/ 
@app.route('/login', methods=['GET', 'POST'])
def login():
    # placeholder values for testing
    test_username = "u1"
    test_password = "p1"

    form = LoginForm()

    if flask.request.method == 'POST' and form.validate_on_submit() :
        if form.username.data == test_username and form.password.data == test_password :
            return(flask.redirect(flask.url_for('session')))

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
    print("here")

    if form.validate_on_submit():
        # Handle form submission
        studentID = form.studentID.data
        consent_status = form.consent_status.data
        sessionID = form.session_id.data

        # Printing for debugging
        print(f"Student ID: {studentID}")
        print(f"Consent Status: {consent_status}")
        print(f"Session ID: {sessionID}")

        # Update student info in database (login/consent)
        # student = GetStudent(studentID=int(studentID))
        
        student = GetStudent(studentID=studentID)[0]

        print(student)
        if student:

            existing_attendance = db.session.query(Attendance).filter_by(studentID=studentID, sessionID=sessionID).first() # should there be a database function for this?

            if existing_attendance:
                flask.flash("User already signed in", category='error')
                return flask.redirect(flask.url_for('home'))
            
            consent_int = 1 if consent_status == "yes" else 0

            student.consent = consent_int
            db.session.commit()

            # Add attendance for the current session
            AddAttendance(attendanceID=None, sessionID=sessionID, studentID=studentID, consent_given=1, facilitatorID=1)
            print(f"Student {studentID} consent status updated to {consent_status}")

            return flask.redirect(flask.url_for('home'))

        else:
            print(f"No student found with ID {studentID}")

    # Redirect back to home page when done
    return flask.redirect(flask.url_for('home'))
    
@app.route('/student_suggestions', methods=['GET'])
def student_suggestions():
    # get the search query from the request
    query = flask.request.args.get('q', '').strip().lower()

    # will need to be replaced with actual session logic later 
    current_session = GetSession(sessionID=1)[0] 

    # get students in the unit associated with the session
    students = GetStudent(unitID=current_session.unitID)

    # filter students based on the query (by name or student number)
    suggestions = []
    for student in students:
        first_last_name = f"{student.firstName} {student.lastName}"
        preferred_last_name = f"{student.preferredName} {student.lastName}"
        if query in student.lastName.lower() or query in student.preferredName.lower() or query in preferred_last_name.lower() or query in str(student.studentNumber):
            suggestions.append({
                'name': f"{student.preferredName} {student.lastName}",
                'id': student.studentID,
                'number': student.studentNumber
            })
        elif query in student.firstName.lower() or query in first_last_name.lower():
            suggestions.append({
                'name': f"{student.firstName} {student.lastName}",
                'id': student.studentID,
                'number': student.studentNumber
            })

    return flask.jsonify(suggestions)
