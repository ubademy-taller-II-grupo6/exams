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
    idtype          = Column(String)
    desc_question   = Column(String)
    answer          = Column(String) 
    true_false      = Column(String)
    desc_choise0    = Column(String)
    answer_choise0  = Column(String)
    desc_choise1    = Column(String)
    answer_choise1  = Column(String)
    desc_choise2    = Column(String)
    answer_choise2  = Column(String)
    desc_choise3    = Column(String)
    answer_choise3  = Column(String)
    desc_choise4    = Column(String)
    answer_choise4  = Column(String)
    desc_choise5    = Column(String)
    answer_choise5  = Column(String)
    desc_choise6    = Column(String)
    answer_choise6  = Column(String)
    desc_choise7    = Column(String)
    answer_choise7  = Column(String)
    desc_choise8    = Column(String)
    answer_choise8  = Column(String)
    desc_choise9    = Column(String)
    answer_choise9  = Column(String)
    