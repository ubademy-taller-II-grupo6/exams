from    sqlalchemy.orm  import Session
import  schema, models

def get_exam_by_id(db: Session, id: int = None):
    if id:
        return db.query (models.Exam).filter(models.Exam.id == id).first()
    
def get_exams_by_creator(db: Session, idcreator: int = None):
    if idcreator:
        return db.query (models.Exam).filter(models.Exam.idcreator == idcreator).all()
        
def create_exam(db: Session, exam: schema.Exam):
    exam_model  = models.Exam(**exam.dict())
    db.add(exam_model)
    db.commit()
    db.refresh(exam_model)
    return exam_model

def update_exam(db: Session, id: int, exam: schema.Exam):
    exam_model                  = models.Exam(**exam.dict())
    exam_to_update              = db.query (models.Exam).filter(models.Exam.id == id).first() 
    exam_to_update.idcreator    = exam_model.idcreator
    exam_to_update.title        = exam_model.title
    exam_to_update.description  = exam_model.description 
    
    db.add(exam_to_update)
    db.commit()
    db.refresh(exam_to_update)
    return exam_to_update

def get_question_by_id (db: Session, idexam: int = None, num_question: int = None):
    if idexam:
        if num_question:  
            return db.query (models.Question).filter(
                             models.Question.idexam == idexam).filter(
                             models.Question.num_question == num_question).first()
                        
def get_questions (db: Session, idexam: int = None):
    if idexam:
        return db.query (models.Question).filter(
                         models.Question.idexam == idexam).all()                        
        
def create_question (db: Session, question: schema.Question):
    question_model  = models.Question(**question.dict())
    db.add(question_model)
    db.commit()
    db.refresh(question_model)
    return question_model

def update_question(db: Session, idexam: int, num_question: int, question: schema.Question):
    question_model              = models.Question(**question.dict())
    question_to_update          = db.query (models.Question).filter( 
                                            models.Question.idexam == idexam).filter(
                                            models.Question.num_question == num_question).first() 
    question_to_update.description      = question_model.description
    
    db.add(question_to_update)
    db.commit()
    db.refresh(question_to_update)
    return question_to_update

def delete_question (db: Session, idexam: int, num_question: int):
    question_to_delete  = db.query( models.Question).filter(
                                    models.Question.idexam  == idexam).filter(
                                    models.Question.num_question == num_question).first() 
    db.delete(question_to_delete)
    db.commit()
    return num_question

def error_message(message):
    return {
        'error': message
    }