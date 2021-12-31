import sqlalchemy
from sqlalchemy.orm import Session
import schema, db_models
from api.src import db
from api.src.exceptions import InvalidOperationException
from api.src.utils import create_message_response


def create_exam(db: Session, exam: schema.Exam):
    course = db.query(db_models.Course).filter(db_models.Course.id == exam.idcourse).first()
    if not course:
        raise InvalidOperationException("El curso no existe")

    if course.creator != exam.idcreator:
        raise InvalidOperationException("El usuario que está intentando crear el examen no es el "
                                        "creador del curso")

    exam_model = db_models.Exam(**exam.dict())
    db.add(exam_model)
    db.commit()
    db.refresh(exam_model)

    response = create_message_response("El examen se creó con éxito")
    return response


def get_exam(db, id_exam, id_creator, id_course):
    query = db.query(db_models.Exam)

    if id_exam:
        query = query.filter(db_models.Exam.idexam == id_exam)

    if id_creator:
        query = query.filter(db_models.Exam.idcreator == id_creator)

    if id_course:
        query = query.filter(db_models.Exam.idcourse == id_course)

    response = query.all()

    if len(response) == 0:
        response = create_message_response("No se encontraron examenes")

    return response


def update_exam(db: Session, exam_id, exam_data: schema.ExamUpdateModel):
    current_exam = db.query(db_models.Exam).filter(db_models.Exam.idexam == exam_id).first()

    if not current_exam:
        raise InvalidOperationException("El examen no existe")

    if current_exam.idcreator != exam_data.id_editor:
        raise InvalidOperationException("La persona que está intentando editar el examen no es el creador del examen")

    current_exam.title = exam_data.title
    current_exam.description = exam_data.description
    current_exam.published = exam_data.published

    db.add(current_exam)
    db.commit()
    db.refresh(current_exam)

    response = create_message_response("El examen se editó con éxito")
    return response


def get_question_by_id(db: Session, idexam: int = None, num_question: int = None):
    if idexam:
        if num_question:
            return db.query(db_models.Question).filter(
                db_models.Question.idexam == idexam).filter(
                db_models.Question.num_question == num_question).first()


def get_questions(db: Session, idexam: int = None):
    exam = db.query(db_models.Exam).filter(db_models.Exam.idexam == idexam).first()
    if not exam:
        raise InvalidOperationException("El examen no existe")

    response = db.query(db_models.Question.num_question, db_models.Question.description).filter(
        db_models.Question.idexam == idexam).order_by(
        db_models.Question.num_question).all()

    if not response:
        response = create_message_response("El examen no tiene preguntas asociadas")

    return response


def store_question_answer(answer: schema.QuestionAnswerModel, db):
    user = db.query(db_models.User).filter(db_models.User.id == answer.id_student).first()

    existing_answer = db.query(db_models.QuestionAnswer).filter(
        db_models.QuestionAnswer.num_question == answer.num_question
        and db_models.QuestionAnswer.id_exam == answer.id_exam
        and db_models.QuestionAnswer.id_student == answer.id_student
    ).first()

    if existing_answer:
        raise InvalidOperationException("El alumno ya respondió a esta pregunta")

    if not user:
        raise InvalidOperationException("El usuario no existe")

    try:
        answer_model = db_models.QuestionAnswer(**answer.dict())
        db.add(answer_model)
        db.commit()

    except sqlalchemy.exc.IntegrityError:
        raise InvalidOperationException("La pregunta no existe")

    response = create_message_response("La respuesta se añadió con éxito")
    return response


def create_question(db: Session, question: schema.Question):
    exam = db.query(db_models.Exam).filter(db_models.Exam.idexam == question.idexam).first()

    if not exam:
        raise InvalidOperationException("El examen no existe")

    if exam.idcreator != question.idcreator:
        raise InvalidOperationException(
            "La persona que está intentando agregar la pregunta no es el creador del examen")

    if question.num_question <= 0:
        raise InvalidOperationException("El numero de pregunta debe ser mayor que 0")

    try:
        question_model = db_models.Question(idexam=question.idexam,
                                            num_question=question.num_question,
                                            description=question.description,
                                            answer=question.answer)
        db.add(question_model)
        db.commit()
        db.refresh(question_model)

    except sqlalchemy.exc.IntegrityError as e:
        raise InvalidOperationException("La pregunta numero " + str(question.num_question) + " ya existe en el examen")

    response = create_message_response("La pregunta se añadió con éxito")

    return response


def update_question(db: Session, idexam: int, num_question: int, question: schema.Question):
    question_model = db_models.Question(**question.dict())
    question_to_update = db.query(db_models.Question).filter(
        db_models.Question.idexam == idexam).filter(
        db_models.Question.num_question == num_question).first()
    question_to_update.description = question_model.description

    db.add(question_to_update)
    db.commit()
    db.refresh(question_to_update)
    return question_to_update


def delete_question(db: Session, idexam: int, num_question: int):
    question_to_delete = db.query(db_models.Question).filter(
        db_models.Question.idexam == idexam).filter(
        db_models.Question.num_question == num_question).first()
    db.delete(question_to_delete)
    db.commit()
    return question_to_delete


def error_message(message):
    return {
        'error': message
    }


def correct_exam(id_exam, id_student, db):
    existing_score = db.query(db_models.ExamScore).filter(
        db_models.ExamScore.id_exam==id_exam and db_models.ExamScore.id_student==id_student).first()

    if existing_score:
        raise InvalidOperationException("El examen ya fue calificado con anterioridad")

    correct_answers = db.query(db_models.Question).filter(db_models.Question.idexam == id_exam).all()

    if not correct_answers:
        raise InvalidOperationException("El examen no existe")

    answers = db.query(db_models.QuestionAnswer).filter(db_models.QuestionAnswer.id_student == id_student).all()

    answers_dict = {}

    for answer in answers:
        answers_dict[answer.num_question] = answer

    score = 0

    for correct_answer in correct_answers:
        try:
            if correct_answer.answer == answers_dict[correct_answer.num_question].answer:
                score += 1
        except:
            continue

    score = (score / len(correct_answers)) * 10

    score_model = db_models.ExamScore(id_exam=id_exam,
                                       id_student=id_student,
                                       score=score
                                       )
    db.add(score_model)

    db.commit()

    return score


def get_score(id_exam, id_student, db):
    score = db.query(db_models.ExamScore).filter(db_models.ExamScore.id_exam == id_exam
                                                 and db_models.ExamScore.id_student == id_student).first()

    if score:
        response = {
            'status': 'CALIFICADO',
            'score': score.score
        }

    else:
        response = {
            'status': 'Sin responder',
            'score': 'Sin responder'
        }

    return response