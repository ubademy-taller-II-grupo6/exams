import  uvicorn
import  os
import  exams_api
from    fastapi                 import FastAPI, Depends, HTTPException
from    fastapi.middleware.cors import CORSMiddleware

from api.src.exception_handlers import add_user_exception_handlers
from    db                      import SessionLocal
from schema import Exam, Question, ExamUpdateModel, QuestionAnswerModel

app = FastAPI()
app.add_middleware( CORSMiddleware, 
                    allow_origins=["*"], 
                    allow_credentials=True, 
                    allow_methods=["*"],
                    allow_headers=["*"],
                    )
add_user_exception_handlers(app)

def db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post('/exams/')
def create_exam(exam: Exam, db=Depends(db)):
    return exams_api.create_exam(db, exam)


@app.get('/exams')
def get_exam(id_exam=None, id_creator=None, id_course=None, db=Depends(db)):
    return exams_api.get_exam(db, id_exam, id_creator, id_course)


@app.put('/exams/{exam_id}')
def update_exam(exam_id , exam_data: ExamUpdateModel, db=Depends(db)):
    return exams_api.update_exam(db, exam_id, exam_data)


@app.post('/exams/questions/')
def create_question(question: Question, db=Depends(db)):
    return exams_api.create_question(db, question)


@app.get('/exams/questions/{idexam}/')
def get_questions(idexam:int, db=Depends(db)):
    return exams_api.get_questions(db, idexam)


@app.post('/exams/questions/answers')
def store_student_answer(answer: QuestionAnswerModel, db=Depends(db)):
    return exams_api.store_question_answer(answer, db)

@app.post('/exams/{id_exam}/{id_student}')
def correct_exam(id_exam, id_student, db = Depends(db)):
    return exams_api.correct_exam(id_exam, id_student, db)

@app.get('/exams/{id_exam}/{id_student}')
def get_score(id_exam, id_student, db = Depends(db)):
    return exams_api.get_score(id_exam, id_student, db)

 

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=int(os.environ.get('PORT')), reload=True)