from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from database import Base


class Employee(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(255))
    login = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    check_admin = Column(Boolean, default=False)


class ApplicationStatus(Base):
    __tablename__ = "application_status"
    id = Column(Integer, primary_key=True)
    name = Column(String(20))   


class PriorityApplication(Base):
    __tablename__ = "priority_application"
    id = Column(Integer, primary_key=True)
    name = Column(String(20))


class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    date_submission = Column(String(255))
    date_completion = Column(String(255))
    cabinet_number = Column(String(50))
    title = Column(String(255))
    problem_description = Column(Text)
    id_employee = Column(Integer, ForeignKey("staff.id"))
    id_priority = Column(Integer, ForeignKey("priority_application.id"))
    id_status = Column(Integer, ForeignKey("application_status.id"))
