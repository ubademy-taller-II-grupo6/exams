from db                  import Base
from sqlalchemy          import Column, Integer, String

class Exam(Base):
    __tablename__   = 'exams'
    id              = Column(Integer, primary_key = True)
    idcreator       = Column(Integer)
    title           = Column(String)
    description     = Column(String)
    
class Question(Base):
    __tablename__   = 'questions'
    idexam          = Column(Integer, primary_key = True)
    num_question    = Column(Integer, primary_key = True)
    description     = Column(String)
    