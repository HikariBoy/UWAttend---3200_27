# UWAttend - Group 27 (CITS3200)

UWAttend is a web-based application written in Flask that is designed to simplify and streamline the process of student sign-ins and sign-outs for university classes. This app helps class facilitators track student participation and manage grading and aims to replace hand-written attendance tracking.

## Manual
For more information on how to use UWAttend, visit the following: [MANUAL.md](MANUAL.md)

## Prerequisites
To run UWAttend on your own machine, you must have the following dependencies installed on your system:

- **Python 3.x:** Required to run the application
- **Pip:** Python's package installer
- **sqlcipher** Required to encrypt and decrypt the database

## Installation
### Clone the Repository
To get started, clone the repository:

``` shell
git clone https://github.com/DeltaO3/UWAttend---3200_27.git UWAttend
cd UWAttend
```

### Setting Up the Environment
1. Create the Python Virtual Environment and activate it:

``` shell
python3 -m venv venv
source /venv/vin/activate
```

2. Install the required dependencies:

``` shell
pip3 install -r requirements.txt
```

3. Setting up .env Secret Keys
UWAttend utilises secret keys located in `.env` for security purposes. Create a file called `.env` in the project root directory and set the following:

``` shell
SECRET_KEY="insert_secret_key_here"
DATABASE_PASSWORD="insert_password_here"
```
*Note: replace `"insert_secret_key_here"` and `"insert_password_here"` with your desired values*

- `SECRET_KEY` - The key to initalise SQLalchemy
- `DATABASE_PASSWORD` - The password that will be used to encrypt `app.db`

### Database Setup
1. Initialise the Database Schema:

``` shell
flask db upgrade
```

2. Populate the Database:

``` shell
python3 -m app.testdb
```

## Running UWAttend
Now that all the dependencies are set up, you can now run the flask app.

To start the web-app, run the following:

``` shell
flask run
```
This will host the application at http://127.0.0.1:5000

## Database Schema

This database schema is designed to manage the different entities and relationships within the **UWAttend** system, such as users, sessions, units, attendance, and student information. Below is an explanation of the purpose of each table and its respective columns.

---

### 1. **alembic_version Table**
- **Purpose**: This table tracks the version of the database schema managed by Alembic (a database migration tool). This helps manage database migrations to ensure the schema is up to date.
- **Columns**:
  - `version_num`: A unique version identifier for the current schema state.

---

### 2. **session Table**
- **Purpose**: This table stores information about individual class sessions for a unit. Each session is linked to a unit and tracks the session name, time, and date.
- **Columns**:
  - `sessionID`: The unique identifier for each session.
  - `unitID`: A foreign key linking to the **unit** table, indicating which unit the session belongs to.
  - `sessionName`: The name of the session (e.g., Lab, Lecture).
  - `sessionTime`: The time when the session takes place (e.g., Morning, Afternoon).
  - `sessionDate`: The date of the session.
  
---

### 3. **Units_Coordinators_Table**
- **Purpose**: This table tracks which users are coordinators for specific units. It links users to units and enforces that only designated coordinators can manage unit-specific tasks.
- **Columns**:
  - `userID`: A foreign key referencing the **user** table, representing the coordinator.
  - `unitID`: A foreign key referencing the **unit** table, indicating which unit the coordinator is responsible for.

---

### 4. **Units_Facilitators_Table**
- **Purpose**: This table tracks which users are facilitators for specific units. Facilitators are responsible for managing sessions and student attendance within the unit.
- **Columns**:
  - `userID`: A foreign key referencing the **user** table, representing the facilitator.
  - `unitID`: A foreign key referencing the **unit** table, indicating which unit the facilitator is assigned to.

---

### 5. **attendance Table**
- **Purpose**: This table logs attendance records for each student in a session, including sign-in and sign-out times, facilitator details, and session-related comments.
- **Columns**:
  - `attendanceID`: The unique identifier for each attendance record.
  - `sessionID`: A foreign key referencing the **session** table, linking the attendance to a specific session.
  - `studentID`: A foreign key referencing the **student** table, identifying the student attending the session.
  - `signInTime`: The time the student signed in for the session.
  - `signOutTime`: The time the student signed out (optional).
  - `facilitatorID`: A foreign key referencing the **user** table (as a facilitator), indicating who facilitated the session.
  - `marks`: Any grades or marks awarded during the session (optional).
  - `comments`: Comments or feedback about the student's participation in the session (optional).
  - `consent_given`: Indicates whether the student has given consent for their participation to be recorded.

---

### 6. **student Table**
- **Purpose**: This table stores information about each student enrolled in a unit, including personal details and consent status.
- **Columns**:
  - `studentID`: The unique identifier for each student.
  - `studentNumber`: The student’s university-assigned number.
  - `firstName`: The student's first name.
  - `lastName`: The student's last name.
  - `title`: The student’s title (e.g., Mr., Ms., Dr.).
  - `preferredName`: The name the student prefers to be called.
  - `unitID`: A foreign key referencing the **unit** table, linking the student to a specific unit.
  - `consent`: Indicates whether the student has provided consent for their participation to be recorded.

---

### 7. **unit Table**
- **Purpose**: This table stores information about the academic units (courses), including session configurations and related settings for the unit.
- **Columns**:
  - `unitID`: The unique identifier for each unit.
  - `unitCode`: The unique code for the course (e.g., CITS3000).
  - `unitName`: The name of the course (e.g., Computing 101).
  - `studyPeriod`: The academic period or semester in which the unit runs.
  - `startDate`: The date when the unit begins.
  - `endDate`: The date when the unit ends.
  - `sessionNames`: Names of the sessions associated with the unit (e.g., Lecture, Lab).
  - `sessionTimes`: Times when the sessions for the unit occur (e.g., Morning, Afternoon).
  - `comments`: A boolean value indicating whether comments are enabled for this unit.
  - `marks`: A boolean value indicating whether marks are assigned for this unit.
  - `consent`: A boolean value indicating whether consent is required for this unit.
  - `commentSuggestions`: Suggested comments that can be used by facilitators for feedback.

---

### 8. **user Table**
- **Purpose**: This table stores information about the users of the system, including administrators, coordinators, and facilitators. Each user has a role and login credentials.
- **Columns**:
  - `userID`: The unique identifier for each user.
  - `userType`: The type of user (e.g., admin, coordinator, facilitator).
  - `firstName`: The first name of the user.
  - `lastName`: The last name of the user.
  - `passwordHash`: The hashed password used for login authentication.
  - `email`: The email address of the user (unique).
  - `token`: Optional field for storing a session or authentication token.
