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

@app.get('/exams/{id}')
def get_exam_by_id (id:int, db=Depends(db)):
    exam = crud.get_exam_by_id(db, id)
    if exam:
        return exam
    else:
        raise HTTPException(404, crud.error_message(f'No existe el examen con id: {id}'))
                    
@app.get('/exams/creators/{idcreator}')
def get_exams_by_creator (idcreator: int, db=Depends(db)):
    exams = crud.get_exams_by_creator(db, idcreator)
    if exams:
        return exams
    else:
        raise HTTPException(404, crud.error_message(f'No existen examenes creados por el creador con id {idcreator}'))

@app.post('/exams/')
def create_exam(exam: Exam, db=Depends(db)):
    return crud.create_exam(db, exam)

@app.put('/exams/')
def update_exam(id: int , exam: Exam, db=Depends(db)):
    exam_exist = crud.get_exam_by_id(db, id)
    if exam_exist is None:
        raise HTTPException(404, detail= crud.error_message(f'No existe el examen con id: {id}'))
    return crud.update_exam(db, id, exam)

@app.get('/exams/questions/')
def get_questions (idexam:int, db=Depends(db)):
    question = crud.get_question_by_id(db, idexam)
    if question:
        return question
    else:
        raise HTTPException(404, crud.error_message(f'No existen preguntas para el examen con id: {idexam} '))

@app.post('/exams/questions/')
def create_question(question: Question, db=Depends(db)):
    return crud.create_question(db, question)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=int(os.environ.get('PORT')), reload=True)        