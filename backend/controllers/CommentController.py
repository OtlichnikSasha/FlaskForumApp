from backend.entities.Comment import Comment
from backend.entities.User import User
from flask import Blueprint, request, session
from app_config import db
from backend.utils import Utils


comment = Blueprint('comment', __name__)

@comment.route('/api/comment/add', methods=['POST'])
def api_comment_add():
    user_id = None
    if 'user_id' in session:
        user_id = session['user_id']
    if user_id == None:
        return Utils.getError("Вы не авторизованы!")
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return Utils.getError("Такого пользователя не найдено!")
    request_data = request.get_json()
    question_id = request_data['question_id']
    text = request_data['text'].strip()
    if len(text) < 10:
        return Utils.getError("Слишком маленький комментарий!")
    comment = Comment(question_id=question_id, author_id=user_id, text=text)
    db.session.add(comment)
    db.session.commit()
    return Utils.getAnswer({})
