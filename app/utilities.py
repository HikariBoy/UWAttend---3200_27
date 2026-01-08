# Utilities file for storing miscellaneous functions that dont neatly fit into other categories
# (i.e. not models, databases, etc)

import csv
import os
import zipfile
import string 
import secrets
from io import StringIO
from app import app, db
from .models import *
from .database import *
from .emails import *
import pandas as pd
from flask_login import current_user
from flask import redirect, url_for

# Custom logging function
def log_message(message):

    client_ip = flask.request.remote_addr 
    
    # Ensure logs directory exists
    if not os.path.exists('logs'):
        os.makedirs('logs')
    # Format the log message with a timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   

    if current_user.is_active:
        formatted_message = f"{client_ip} {current_user.firstName} {current_user.lastName} {timestamp} - {message}\n"
    else:
        formatted_message = f"{client_ip} {timestamp} - {message}\n"
    
    # Write the log message to a file
    with open('logs/app.log', 'a') as log_file:
        log_file.write(formatted_message)

    # Print the log message to the console
    print(formatted_message)


def database_error(route, db_table) :

    log_message('/' + route + " Error loading " + db_table)
    flask.flash("Error - please try again", 'error')

def access_error(route, db_table) :
    log_message('/' + route + " User can't access " + db_table)
    flask.flash("Error - please try again", 'error')


# Set of functions used to read and populate students into the database from a csv file.
# Checklist for future
# 1. DONE Connect to actual database for population
# 2. DONE Create upload button for frontend that uses these functions
# 3. DONE Remove "if __name__ == "__main__:" and instead incorporate code into Flask

# Reads a CSV file and returns a list of dictionaries where each dictionary represents a row.
def read_csv_file(file_path):
    data = []
    if os.path.exists(file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    else:
        print(f"The file {file_path} does not exist.")
    return data

# Imports students into the database given a .csv file
def import_student_in_db(data, unit_id):

    unit = GetUnit(unitID=unit_id)

    if not unit:
        print("Student cannot be added to unit until unit is initialised")
        return
    
    unit = unit[0]

    for record in data:

        student_number = record['Student ID']
        if student_exists(student_number, unit_id):
            print(f"Duplicate found: {record['Given Names']} {record['Surname']} (ID: {student_number}) - Skipping import.")
            continue

        # Call the AddStudent function from database.py
        AddStudent(
            studentNumber=record['Student ID'],
            firstName=record['Given Names'],
            lastName=record['Surname'],
            title=record['Title'],
            preferredName=record['Preferred Name'],
            unitID=unit_id,  # Assuming a default unit ID, replace as needed
            consent='no' if unit.consent else 'not required' # Setting consent to no as per your requirements
        )
        print(f"Added student: {record['Given Names']} {record['Surname']} (ID: {student_number})")

def import_facilitator_in_db(data, unit_id, current_user):

    for record in data:        
        facilitator = record['Facilitator Email']
        
        #Add facilitator as user if not in DB
        if(not GetUser(email=facilitator)):
            temp_password = generate_temp_password()
            print(f"Adding new user: {facilitator}")
            AddUser(facilitator, "placeholder", "placeholder", temp_password, "facilitator")
            send_email_ses("noreply@uwaengineeringprojects.com", facilitator, 'welcome')
        # add this unit to facilator
        if(facilitator == current_user.email):
            print(f"skipping user {facilitator} as it is the currently logged in user.")
            continue
        print(f"Adding unit {unit_id} to facilitator {facilitator}")
        AddUnitToFacilitator(facilitator, unit_id)

def generate_temp_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

# Process a .csv file by reading and then importing into "student" table. 
# If current user is passsed, processes file as a facilitator file
def process_csvs(student_file_path, facilitator_file_path):
    with app.app_context():
        # Read the data from the CSV file
        s_data = read_csv_file(student_file_path)
        if facilitator_file_path is not None:
            f_data = read_csv_file(facilitator_file_path)
        else:
            f_data = False
        if s_data and f_data:
            # Import the data to the database
            #Ensure passed csv file is correct type 
            errors = validate_csv_headers(s_data[0], f_data[0])

            if errors:
                msg = ''
                for error in errors :
                    msg += error + ', '
                return 0, 0, msg[:-2]
            return s_data, f_data, 0 #return value for routes validation
        if s_data and facilitator_file_path is None:
            if len(s_data[0]) != 5:
                print("Not a student csv!")
                return 0, "Student csv format is incorrect"
            else:
                return s_data, 0

# checks if headers are correct based on first row only
def validate_csv_headers(s_data_row, f_data_row) :

    errors = []

    if len(s_data_row) != 5:
        print("Not a student csv!")
        errors.append("Student csv format is incorrect")
    if len(f_data_row) != 1:
        print("Not a facilitator csv!")
        errors.append("Facilitator csv format is incorrect")

    student_headers = ["Student ID", "Surname", "Title", "Given Names", "Preferred Name"]
    factilitator_headers = ["Facilitator Email"]

    for header in student_headers :
        if header not in s_data_row :
            errors.append(f"{header} header not detected in student csv")

    for header in factilitator_headers :
        if header not in f_data_row :
            errors.append(f"{header} header not detected in facilitator csv")

    return errors


# Export a table to csv
def exportTableToCSV(records) :

    # Get the column names from the model's attributes
    columns = records[0].__table__.columns.keys()

    # If exporting the User table, exclude the passwordHash column
    columns = [col for col in columns if col not in ['passwordHash', 'token']]

    # Use StringIO to write CSV data in-memory
    csvfile = StringIO()
    writer = csv.writer(csvfile)
    writer.writerow(columns)  # Write the header

    # Write each record as a row in the CSV
    for record in records:
        writer.writerow([getattr(record, col) for col in columns])

    return csvfile.getvalue()

def exportAttendanceFullDetailToCSV(records) :

    columns = [
        'studentNumber', 'firstName', 'lastName', 'title', 'preferredName', 'unitCode',
        'sessionDate', 'sessionName', 'sessionTime', 'signInTime', 'signOutTime',
        'marks', 'comments', 'consent', 'signedInBy'
    ]

    csvfile = StringIO()
    writer = csv.writer(csvfile)
    writer.writerow(columns)  # Write the header

    # Iterate over each record and write to csvfile
    for attendance, student, session, unit, user in records:
        row = [
            student.studentNumber,
            student.firstName,
            student.lastName,
            student.title,
            student.preferredName,
            unit.unitCode,
            session.sessionDate.strftime('%Y-%m-%d') if session.sessionDate else '',
            session.sessionName,
            session.sessionTime,
            attendance.signInTime.strftime('%H:%M:%S') if attendance.signInTime else '',
            attendance.signOutTime.strftime('%H:%M:%S') if attendance.signOutTime else '',
            attendance.marks if attendance.marks else '', # Marks, blank if none
            attendance.comments if attendance.comments else '', # Comments, blank if none
            attendance.consent_given, # Consent give: yes, no or not required (if unit is configured to not ask consent)
            user.firstName + " " + user.lastName
        ]
        writer.writerow(row)

    return csvfile.getvalue()

def exportAttendanceFullDetailToCSVCOLUMNS(records) :
    
    # Initialize a dictionary to store students, keyed by (studentNumber, unitCode) for uniqueness per unit
    attendance_data = {}

    # Iterate over the records and organize by unique student-unit combinations
    for attendance, student, session, unit, facilitator in records:
        # Use a tuple (studentNumber, unitCode) as the key to ensure uniqueness per unit
        unique_key = (student.studentNumber, unit.unitCode)
        if unique_key not in attendance_data:
            attendance_data[unique_key] = {
                'studentNumber': student.studentNumber,
                'firstName': student.firstName,
                'lastName': student.lastName,
                'title': student.title,
                'preferredName': student.preferredName,
                'unitCode': unit.unitCode
            }

        # Format session data for attendance: [sessionName][FacilitatorName]signInTime;signOutTime
        session_key = f"{session.sessionDate.strftime('%Y_%B_%d')}_{session.sessionTime}"
        sign_in_time = (
            attendance.signInTime.strftime('%H:%M:%S')
            if attendance.signInTime
            else ''
        )
        sign_out_time = (
            attendance.signOutTime.strftime('%H:%M:%S')
            if attendance.signOutTime
            else ''
        )
        facilitator_name = f"{facilitator.firstName} {facilitator.lastName}"
        consent_status = "yes" if attendance.consent_given == "yes" else "no"
        attendance_info = f"[{session.sessionName}][{facilitator_name}]{sign_in_time};{sign_out_time};consent_given={consent_status}"

        # Store attendance_info under session_key
        if (session_key in attendance_data[unique_key]) :
            attendance_data[unique_key][session_key] += "," + attendance_info
        else :
            attendance_data[unique_key][session_key] = attendance_info

        # Format grade data according to your specified rules
        marks = attendance.marks if attendance.marks else ''
        comments = attendance.comments if attendance.comments else ''

        if marks and comments:
            grade_info = f"{marks};comment={comments}"
        elif marks:
            grade_info = f"{marks};"
        elif comments:
            grade_info = f";comment={comments}"
        else:
            grade_info = ''

        if (grade_info != '') :
            # Store grade_info under session_key + '_Grade'
            if (f"{session_key}_Grade" in attendance_data[unique_key]) :
                attendance_data[unique_key][f"{session_key}_Grade"] += "," + session.sessionName + ":" + grade_info
            else :
                attendance_data[unique_key][f"{session_key}_Grade"] = session.sessionName + ":" + grade_info

    # Prepare the headers
    headers = [
        'studentNumber', 'firstName', 'lastName', 'title', 'preferredName', 'unitCode'
    ]

    # Collect all session_keys
    session_keys = set()
    for student_record in attendance_data.values():
        for key in student_record:
            if key not in headers:
                if key.endswith('_Grade'):
                    session_keys.add(key[:-6])  # Remove '_Grade' from key
                else:
                    session_keys.add(key)

    # Sort the session_keys and build headers
    sorted_session_keys = sorted(session_keys)

    for session_key in sorted_session_keys:
        headers.append(session_key)
        headers.append(f"{session_key}_Grade")

    # Create a list of rows (each row represents a unique student-unit combination)
    rows = []
    for student_unit_key, student_record in attendance_data.items():
        # Print the student record before creating the row
        row = [student_record.get(header, '') for header in headers]
        rows.append(row)

    # Convert to CSV with proper quoting
    csvfile = StringIO()
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(headers)  # Write the header
    writer.writerows(rows)    # Write all student rows

    return csvfile.getvalue()


#Export unit data to a ZIP file containing multiple CSV files
def exportUnitToZip(zip_filename, unitID, unitCode, zipf) :

        student_records = GetStudent(unitID=unitID)
        if not student_records :
            print("no student records found")
        else :
            student_csv = exportTableToCSV(student_records)
            zipf.writestr(unitCode + '_students.csv', student_csv)

        user_records = GetUsersForUnit(unitID)
        if not user_records :
            print("no user records founds")
        else :
            user_csv = exportTableToCSV(user_records)
            zipf.writestr(unitCode + '_users.csv', user_csv)
        
        attendance_records = GetAttendancesForUnit(unitID)
        if not attendance_records :
            print("no attendance records found")
        else :
            attendance_csv = exportTableToCSV(attendance_records)
            zipf.writestr(unitCode + '_attendance.csv', attendance_csv)

        session_records = GetSessionForExport(unitID=unitID)
        if not session_records :
            print("no session records found")
        else :
            session_csv = exportTableToCSV(session_records)
            zipf.writestr(unitCode + '_session.csv', session_csv)

        unit_records = GetUnit(unitID=unitID)
        if not unit_records :
            print("no unit records found")
        else :
            unit_csv = exportTableToCSV(unit_records)
            zipf.writestr(unitCode + '_unit.csv', unit_csv)

        attendance_full_detail_records = GetAttendancesForUnitFullDetail(unitID)
        if not attendance_full_detail_records :
            print("no attendance_full_detail records found")
        else :
            # export as one attendance per row
            attendance_full_detail_csv = exportAttendanceFullDetailToCSV(attendance_full_detail_records)
            zipf.writestr(unitCode + '_attendance_full_detail.csv', attendance_full_detail_csv)

            # export as one student per row (COLUMNS csv)
            attendance_full_detail_COLUMNS_csv = exportAttendanceFullDetailToCSVCOLUMNS(attendance_full_detail_records)
            zipf.writestr(unitCode + '_attendance_full_detailCOLUMNS.csv', attendance_full_detail_COLUMNS_csv)


# Helper function to get the unitID from a unitCode
def get_unit_id_by_code(unit_code):
    unit = db.session.query(Unit).filter_by(unitCode=unit_code).first()
    if unit:
        return unit.unitID
    return None

# Function to check user access
def userHasFacilitatorAccessToUnit(unit=None) :

    if unit is None :
        return False

    if unit in current_user.unitsFacilitate :
        return True
    return False

def userHasCoordinatorAccessToUnit(unit) :

    if unit is None :
        return False
    
    if unit in current_user.unitsCoordinate :
        return True
    return False

def userHasCoordinatorAccessToUnitByID(unit_id) :
    
    for u in current_user.unitsCoordinate :
        try :
            if u.unitID == int(unit_id) :
                return True
        except :
            return False
        
    return False

def userHasFacilitatorAccessToUnitByID(unit_id) :
    
    for u in current_user.unitsFacilitate :
        try :
            if u.unitID == int(unit_id) :
                return True
        except :
            return False

    return False


def userHasAccessToSession(session) :

    if session is None :
        return False

    for u in current_user.unitsFacilitate :
        if u.unitID == session.unitID :
            return True
    return False

def sessionDetailsAreValid(unit, sessionName, sessionTime) :
    if unit is None :
        return False
    
    if sessionName in unit.sessionNames.split('|') and sessionTime in unit.sessionTimes.split('|') :
        return True