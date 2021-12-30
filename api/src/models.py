from sqlalchemy.sql.sqltypes import BOOLEAN
from db                  import Base
from sqlalchemy          import Column, Integer, String

class Exam(Base):
    __tablename__   = 'exams'
    idexam          = Column(Integer, primary_key = True)
    idcreator       = Column(Integer)
    idcourse        = Column(Integer)
    title           = Column(String)
    description     = Column(String)
    
class Question(Base):
    __tablename__   = 'questions'
    idexam          = Column(Integer, primary_key = True)
    num_question    = Column(Integer, primary_key = True)
    description     = Column(String)
    answer          = Column(BOOLEAN)
    