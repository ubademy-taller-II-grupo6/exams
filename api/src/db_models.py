from sqlalchemy.sql.sqltypes import BOOLEAN, Boolean, Numeric
from db import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Exam(Base):
    __tablename__ = 'exams'
    idexam = Column(Integer, primary_key=True)
    idcreator = Column(Integer)
    idcourse = Column(Integer)
    title = Column(String)
    description = Column(String)
    published = Column(Boolean)


class Question(Base):
    __tablename__ = 'questions'
    idexam = Column(Integer, primary_key=True)
    num_question = Column(Integer, primary_key=True)
    description = Column(String)
    answer = Column(Boolean)


class QuestionAnswer(Base):
    __tablename__ = 'questions_answers'
    id_student = Column(Integer, primary_key=True)
    id_exam = Column(Integer, primary_key=True)
    num_question = Column(Integer, primary_key=True)
    answer = Column(Boolean)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    lastname = Column(String)
    email = Column(String)
    blocked = Column(Boolean)


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    hashtags = Column(String)
    type = Column(String)
    category = Column(String)
    exams = Column(Integer)
    subscription = Column(String)
    location = Column(String)
    creator = Column(Integer, ForeignKey(User.id))
    enrollment_conditions = Column(String)
    unenrollment_conditions = Column(String)


class ExamScore(Base):
    __tablename__ = 'exam_scores'
    id_exam = Column(Integer, primary_key=True)
    id_student = Column(String, primary_key=True)
    score = Column(Numeric)

