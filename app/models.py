from typing import List, Optional
from datetime import date, time
from sqlalchemy import ForeignKey, Column, Table, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app import db
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash

# Define association tables
Units_Coordinators_Table = db.Table(
    'Units_Coordinators_Table',
    Column('userID', Integer, ForeignKey('user.userID'), primary_key=True),
    Column('unitID', Integer, ForeignKey('unit.unitID'), primary_key=True)
)

Units_Facilitators_Table = db.Table(
    'Units_Facilitators_Table',
    Column('userID', Integer, ForeignKey('user.userID'), primary_key=True),
    Column('unitID', Integer, ForeignKey('unit.unitID'), primary_key=True)
)

# Define models
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    userID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    firstName: Mapped[Optional[str]] = mapped_column(String(50))
    lastName: Mapped[Optional[str]] = mapped_column(String(50))
    passwordHash: Mapped[str] = mapped_column(String(256), nullable=False)
    userType: Mapped[str] = mapped_column(String((15)), nullable=False)   # "admin", "coordinator", "facilitator"
    token: Mapped[Optional[str]] = mapped_column(String((256)))

    unitsCoordinate: Mapped[List['Unit']] = relationship(secondary='Units_Coordinators_Table', back_populates='coordinators')
    unitsFacilitate: Mapped[List['Unit']] = relationship(secondary='Units_Facilitators_Table', back_populates='facilitators')

    def get_id(self):
        return str(self.userID)
    
    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.passwordHash, password_plaintext)

    def set_password(self, password_plaintext: str):
        self.passwordHash = generate_password_hash(password_plaintext)
    
class Unit(db.Model) :
    __tablename__ = 'unit'
    unitID: Mapped[int] = mapped_column(primary_key=True)
    unitCode: Mapped[str] = mapped_column(String(50), nullable=False)
    unitName: Mapped[str] = mapped_column(String(50), nullable=False)
    studyPeriod: Mapped[str] = mapped_column(String(50), nullable=False)
    startDate: Mapped[date] = mapped_column(nullable=False)
    endDate: Mapped[date] = mapped_column(nullable=False)

    coordinators: Mapped[List['User']] = relationship(secondary='Units_Coordinators_Table', back_populates='unitsCoordinate')
    facilitators: Mapped[List['User']] = relationship(secondary='Units_Facilitators_Table', back_populates='unitsFacilitate')
    students: Mapped[List['Student']] = relationship()

    sessionNames: Mapped[str] = mapped_column(String(2000), nullable=False)     # | separated string
    sessionTimes: Mapped[str] = mapped_column(String(2000), nullable=False)     # | separated string
    comments: Mapped[bool] = mapped_column(nullable=False)
    marks: Mapped[bool] = mapped_column(nullable=False)
    consent: Mapped[bool] = mapped_column(nullable=False)
    commentSuggestions: Mapped[Optional[str]] = mapped_column(String(2000))     # | separated string

class Student(db.Model) :
    __tablename__ = 'student'
    studentID: Mapped[int] = mapped_column(primary_key=True)
    studentNumber: Mapped[str] = mapped_column(String(15), nullable=False)
    firstName: Mapped[str] = mapped_column(String(50), nullable=False)
    lastName: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    preferredName: Mapped[str] = mapped_column(String(50), nullable=False)
    unitID: Mapped[int] = mapped_column(ForeignKey('unit.unitID'), nullable=False)
    consent: Mapped[str] = mapped_column(String(50), nullable=False)    # "yes", "no", "not required"

class Session(db.Model) :
    __tablename__ = 'session'
    sessionID: Mapped[int] = mapped_column(primary_key=True)
    unitID: Mapped[int] = mapped_column(ForeignKey('unit.unitID'), nullable=False)
    sessionName: Mapped[str] = mapped_column(String(50), nullable=False)
    sessionTime: Mapped[str] = mapped_column(String(50), nullable=False)
    sessionDate: Mapped[date] = mapped_column(nullable=False)

class Attendance(db.Model) :
    __tablename__ = 'attendance'
    attendanceID: Mapped[int] = mapped_column(primary_key=True)
    sessionID: Mapped[int] = mapped_column(ForeignKey('session.sessionID'), nullable=False)
    studentID: Mapped[int] = mapped_column(ForeignKey('student.studentID'), nullable=False)
    signInTime: Mapped[time] = mapped_column(nullable=False)
    signOutTime: Mapped[time] = mapped_column(nullable=True)
    facilitatorID: Mapped[int] = mapped_column(ForeignKey('user.userID'), nullable=False)
    marks: Mapped[Optional[str]] = mapped_column(String(100))         # | separated string
    comments: Mapped[Optional[str]] = mapped_column(String(1000))     # | separated string
    consent_given: Mapped[str] = mapped_column(String(50), nullable=False)  # "yes", "no", "not required"


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


