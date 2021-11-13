from pydantic                   import BaseModel
        
class Exam (BaseModel):
    idcreator               :   int
    title                   :   str
    description             :   str
    class Config:
        orm_mode = True        
        
class Question(BaseModel):
    idexam                  :   int
    num_question            :   int
    idtype                  :   str
    desc_question           :   str
    answer                  :   str
    true_false              :   str
    desc_choise0            :   str
    answer_choise0          :   str
    desc_choise1            :   str
    answer_choise1          :   str
    desc_choise2            :   str
    answer_choise2          :   str
    desc_choise3            :   str
    answer_choise3          :   str
    desc_choise4            :   str
    answer_choise4          :   str    
    desc_choise5            :   str    
    answer_choise5          :   str
    desc_choise6            :   str    
    answer_choise6          :   str    
    desc_choise7            :   str
    answer_choise7          :   str
    desc_choise8            :   str
    answer_choise8          :   str
    desc_choise9            :   str
    answer_choise9          :   str