from backend.entities.Question import Question
from backend.entities.User import User
from backend.entities.Question_cat import Question_cat
from flask import Blueprint, request, session
from app_config import db
from backend.utils import Utils


question = Blueprint('question', __name__)

@question.route('/api/question/create', methods=['POST'])
def api_question_create():
    user_id = None
    if 'user_id' in session:
        user_id = session['user_id']
    if user_id == None:
        return Utils.getError("Вы не авторизованы!")
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return Utils.getError("Такого пользователя не найдено!")
    request_data = request.get_json()
    text = request_data['question'].strip()
    tags = request_data['tags']
    title = request_data['title'].strip()
    if title == '':
        return Utils.getError("Вы не ввели тему вопроса")
    question = Question(title=title, text=text, author_id=user_id)
    db.session.add(question)
    db.session.commit()
    for tag in tags:
        qc = Question_cat(question_id=question.id, category_id=tag)
        db.session.add(qc)
        db.session.commit()
    return Utils.getAnswer({'question': question.id})




