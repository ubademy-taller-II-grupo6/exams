import  uvicorn
import  os
import  crud
from    fastapi                 import FastAPI, Depends, HTTPException
from    fastapi.middleware.cors import CORSMiddleware
from    db                      import SessionLocal
from    schema                  import Exam, Question      
                                
app = FastAPI()
app.add_middleware( CORSMiddleware, 
                    allow_origins=["*"], 
                    allow_credentials=True, 
                    allow_methods=["*"],
                    allow_headers=["*"],
                    )

def db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get('/exams/{idexam}')
def get_exam_by_id (idexam:int, db=Depends(db)):
    exam = crud.get_exam_by_id(db, idexam)
    if exam:
        return exam
    else:
        raise HTTPException(404, crud.error_message(f'No existe el examen con id: {idexam}'))
                    
@app.get('/exams/creators/{idcreator}/')
def get_exams_by_creator (idcreator: int, db=Depends(db)):
    exams = crud.get_exams_by_creator(db, idcreator)
    if exams:
        return exams
    else:
        raise HTTPException(404, crud.error_message(f'No existen examenes creados por el creador con id {idcreator}'))

@app.get('/exams/courses/{idcourse}/')
def get_exams_by_course (idcourse: int, db=Depends(db)):
    exams = crud.get_exams_by_course(db, idcourse)
    if exams:
        return exams
    else:
        raise HTTPException(404, crud.error_message(f'No existen examenes para el curso con id {idcourse}'))

@app.post('/exams/')
def create_exam(exam: Exam, db=Depends(db)):
    return crud.create_exam(db, exam)

@app.put('/exams/')
def update_exam(idexam: int , exam: Exam, db=Depends(db)):
    exam_exists = crud.get_exam_by_id(db, idexam)
    if exam_exists is None:
        raise HTTPException(404, detail= crud.error_message(f'No existe el examen con id: {idexam}'))
    return crud.update_exam(db, idexam, exam)

@app.get('/exams/{idexam}/questions/')
def get_questions (idexam:int, db=Depends(db)):
    question = crud.get_questions(db, idexam)
    if question:
        return question
    else:
        raise HTTPException(404, crud.error_message(f'No existen preguntas para el examen con id: {idexam} '))

@app.get('/exams/{idexam}/questions/{num_question}')
def get_question_by_id (idexam:int, num_question: int, db=Depends(db)):
    question = crud.get_question_by_id(db, idexam, num_question)
    if question:
        return question
    else:
        raise HTTPException(404, crud.error_message(f'No existen la pregunta número {num_question} para el examen con id: {idexam} '))

@app.post('/exams/questions/')
def create_question(question: Question, db=Depends(db)):
    return crud.create_question(db, question)

@app.delete('/exams/{idexam}/questions/{num_question}/')
def delete_question(idexam:int, num_question:int, db=Depends(db)):
    question = crud.get_question_by_id(db,idexam, num_question)
    if question:
        return crud.delete_question(db, idexam, num_question)
    else:     
        raise HTTPException(404, crud.error_message(f'No existen la pregunta número {num_question} para el examen con id: {idexam} '))
 

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=int(os.environ.get('PORT')), reload=True)        