from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .db import Base
# from ORM_and_SQLAlchemy.db import Base



url = f'postgresql://postgres:14021992@localhost:5432/postgres'
Base = declarative_base()
engine = create_engine(url, echo=False, pool_size=5)

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(120), nullable=False)
    disciplines = relationship('Discipline', backref='teacher')

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    students = relationship('Student', backref='group')

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(120), nullable=False)
    group_id = Column('group_id', ForeignKey('groups.id', ondelete='CASCADE'))


class Discipline(Base):
    __tablename__ = 'disciplines'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    teacher_id = Column('teacher_id', ForeignKey('teachers.id', ondelete='CASCADE'))
    grades = relationship('Grade', backref='discipline')


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    date_received = Column(Date, nullable=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    discipline_id = Column(Integer, ForeignKey('disciplines.id', ondelete='CASCADE'))
    student = relationship('Student', backref='grades')
