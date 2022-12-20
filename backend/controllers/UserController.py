from backend.entities.User import User
from flask import Blueprint, request, session
from app_config import db
from backend.utils import Utils

user = Blueprint('user', __name__)


@user.route('/api/user/edit')
def api_user_edit():
    description = request.values.get('description', '', str)
    user_id = None
    if 'user_id' in session:
        user_id = session['user_id']
    if user_id == None:
        return Utils.getError("Вы не авторизованы!")
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return Utils.getError("Такого пользователя не найдено!")
    user.description = description
    db.session.commit()
    return Utils.getAnswer({'user_description': user.description})

