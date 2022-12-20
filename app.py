from flask import Flask, render_template, redirect, request, session
from app_config import app, db
from backend.utils import Utils
from backend.entities.User import User
from backend.entities.Category import Category
from backend.entities.Comment import Comment
from backend.entities.Question import Question
from backend.entities.Question_cat import Question_cat


from backend.controllers.UserController import user
from backend.controllers.QuestionController import question
from backend.controllers.TagsController import tags
from backend.controllers.CommentController import comment

import math

app.secret_key = 'EducationalProject'
app.register_blueprint(user)
app.register_blueprint(question)
app.register_blueprint(tags)
app.register_blueprint(comment)
#
# db.create_all()
@app.route('/', defaults={'page': 1})
@app.route('/page')
def index(page):
    user = None
    if 'user_id' in session:
        user = session['user_id']
    page = int(page)
    item_count = page * 15
    skip_count = item_count - 15
    tags = []
    tag = []
    page_count = math.ceil((Question.query.count() / 15))
    questions = Question.query.order_by(Question.id.desc()).limit(
        item_count).offset(skip_count).all()
    for question in questions:
        question.cats = Question_cat.query.filter_by(question_id=question.id).all()
        for quest in question.categories:
            if quest.category_id in tags:
                continue
            else:
                tags.append(quest.category_id)
    for c in tags:
        category = Category.query.filter_by(id=c).first()
        tag.append(category)
    categories = Category.query.order_by(Category.views).limit(
        15).all()
    return render_template('site/index.html', questions=questions, tags=tag, user=user, categories=categories,
                           page=page, page_count=page_count)


@app.route('/questions/<cat_link>', defaults={'page': 1})
@app.route('/questions/<cat_link>/page')
def questions(cat_link, page):
    user = None
    if 'user_id' in session:
        user = session['user_id']
    page = int(page)
    item_count = page * 15
    skip_count = item_count - 15
    page_count = math.ceil((Question.query.count() / 15))
    questions = []
    print(cat_link)
    category = Category.query.filter_by(id=cat_link).first()
    category.views += 1
    db.session.commit()
    questions_id = Question_cat.query.filter_by(category_id=category.id).order_by(Question_cat.id.desc()).limit(
        item_count).offset(skip_count).all()
    for quest in questions_id:
        questions.append(Question.query.filter_by(id=quest.question_id).first())
    for quests in questions:
        quests.cats = Question_cat.query.filter_by(question_id=quests.id).all()
    categories = Category.query.filter(Category.title != cat_link).order_by(Category.views).limit(
        15).all()

    return render_template('site/questions.html', questions=questions, user=user, categories=categories,
                           category=category, page=page, page_count=page_count)


@app.route('/question/<id>')
def question(id):
    user = None
    if 'user_id' in session:
        user = session['user_id']
    question = Question.query.filter_by(id=id).first()
    question.views += 1
    db.session.commit()
    similar_questions = []
    questions_id = []
    tag = []
    comments = Comment.query.filter_by(question_id=id).all()
    for quest in question.categories:
        category = Category.query.filter_by(id=quest.category_id).first()
        tag.append(category)
        questions_id = Question_cat.query.filter(Question_cat.question_id != question.id).filter_by(
            category_id=quest.category_id).limit(10).all()
    for q in questions_id:
        similar_questions.append(Question.query.filter_by(id=q.question_id).first())
    return render_template("site/question.html", question=question, similar_questions=similar_questions, user=user, comments=comments, tags=tag)


@app.route('/categories', defaults={'page': 1})
@app.route('/categories/<page>')
def categories(page):
    page = int(page)
    user = None
    if 'user_id' in session:
        user = session['user_id']
    page = int(page)
    item_count = page * 15
    skip_count = item_count - 15
    page_count = math.ceil((Category.query.count() / 15))
    categories = Category.query.order_by(Category.views).limit(
        item_count).offset(skip_count).all()
    for cat in categories:
        cat.question_count = Question_cat.query.filter_by(category_id=cat.id).count()
    return render_template('site/categories.html', categories=categories, user=user, page=page, page_count=page_count)


@app.route('/users', defaults={'page': 1})
@app.route('/users/<page>')
def users(page):
    page = int(page)
    user = None
    if 'user_id' in session:
        user = session['user_id']
    page = int(page)
    item_count = page * 15
    skip_count = item_count - 15
    page_count = math.ceil((User.query.count() / 15))
    users = User.query.order_by(User.id.desc()).limit(
        item_count).offset(skip_count).all()
    for user in users:
        user.comment_count = Comment.query.filter_by(author_id=user.id).count()
        user.question_count = Question.query.filter_by(author_id=user.id).count()
    return render_template('site/users.html', users=users, user=user, page=page, page_count=page_count)


@app.route('/add_question')
def add_question():
    user = None
    if 'user_id' in session:
        user = session['user_id']
    return render_template('site/addQuestion.html', user=user)


@app.route('/search/<name>')
def search(name):
    user = None
    if 'user_id' in session:
        user = session['user_id']
    category = Category.query.filter(Category.title.contains(name)).order_by(Category.id.desc()).all()
    questions_id = []
    for cat in category:
        questions_id = Question_cat.query.filter_by(category_id=cat.id).all()
    questions = []
    for question in questions_id:
        questions.append(Question.query.filter_by(id=question.question_id).first())
    for quests in questions:
        quests.cats = Question_cat.query.filter_by(question_id=quests.id).all()
    return render_template("site/search.html", questions=questions, user=user, name=name)


@app.route('/login/authorization')
def authorization_page():
    return render_template('site/auth.html')


@app.route('/login/signup')
def signup_page():
    return render_template('site/signup.html')

@app.route('/cabinet')
def cabinet():
    user = None
    if 'user_id' in session:
        user = session['user_id']
    if user == None:
        return redirect('/login/authorization', code=302)
    cabinet_user = User.query.filter_by(id=user).first()
    comment_count = Comment.query.filter_by(author_id=cabinet_user.id).count()
    question_count = Question.query.filter_by(author_id=cabinet_user.id).count()
    cabinet_user.statistics['comment_count'] = comment_count
    cabinet_user.statistics['question_count'] = question_count
    return render_template('site/cabinet.html', user=cabinet_user)

@app.route('/user/<id>')
def user(id):
    id = int(id)
    user = User.query.filter_by(id=id).first()
    comment_count = Comment.query.filter_by(author_id=user.id).count()
    question_count = Question.query.filter_by(author_id=user.id).count()
    user.statistics['comment_count'] = comment_count
    user.statistics['question_count'] = question_count
    return render_template('site/user.html', user=user)


# Authorization
@app.route('/api/user/authorization', methods=['POST'])
def api_user_auth():
    request_data = request.get_json()
    login = request_data['login'].strip()
    password = request_data['password'].strip()
    user = User.query.filter_by(login=login).first()
    if user is None:
        return Utils.getError('User with this login was not found')
    if user.password != Utils.get_hash(password):
        return Utils.getError('Password is no correct')
    if 'user_id' not in session:
        session['user_id'] = user.id
    return Utils.getAnswer({'id': user.id})


@app.route('/api/user/registration', methods=['POST'])
def api_user_registration():
    request_data = request.get_json()
    login = request_data['login'].strip()
    already_user = User.query.filter_by(login=login).first()
    if already_user is not None:
        return Utils.getError("User with this login already registration")
    password = request_data['password'].strip()
    if len(password) < 6:
        return Utils.getError("Password is no correct")
    password = Utils.get_hash(password)
    user = User(login=login, password=password, description='')
    db.session.add(user)
    db.session.commit()
    return Utils.getAnswer({})


@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.modified = True
        for key in list(session.keys()):
            session.pop(key)
        session.modified = True
    return redirect('/')


if __name__ == '__main__':
    app.run()
