from pydantic                   import BaseModel
        
class Exam (BaseModel):
    idcreator               :   int
    idcourse                :   int
    title                   :   str
    description             :   str
    class Config:
        orm_mode = True        
        
class Question(BaseModel):
    idexam                  :   int
    num_question            :   int
    description             :   str
    answer                  :   bool
    class Config:
        orm_mode = True