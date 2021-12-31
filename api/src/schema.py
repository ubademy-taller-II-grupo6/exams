from pydantic import BaseModel


class Exam(BaseModel):
    idcreator: int
    idcourse: int
    title: str
    description: str
    published: bool



class ExamUpdateModel(BaseModel):
    id_editor: int
    title: str
    description: str
    published: bool


class Question(BaseModel):
    idexam: int
    idcreator: int
    num_question: int
    description: str
    answer: bool

class QuestionAnswerModel(BaseModel):
    id_exam: int
    id_student: int
    num_question: int
    answer: bool

class ScoreModel(BaseModel):
    status: str
    score: float
