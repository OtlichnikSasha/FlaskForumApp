import json
import logging
from flask import Response, Blueprint
from backend.entities.User import User
from backend.entities.Category import Category
from backend.entities.Comment import Comment
from backend.entities.Question import Question
from backend.entities.Question_cat import Question_cat
import re
import hashlib


util_app = Blueprint('util_app', __name__)


def getError(error_text):
    res = {
        'status': 'error',
        'message': error_text
    }
    return Response(
        response=json.dumps(res, ensure_ascii=False),
        mimetype='application/json',
        status=200
    )


def getAnswer(text, info=None):
    if info is None:
        info = {}
    res = {
        'status': 'ok',
        'message': text
    }
    answer = {**res, **info}
    return Response(
        response=json.dumps(answer, ensure_ascii=False, default=json_serial),
        mimetype='application/json',
        status=200
    )


def products_comparison(p_one, p_two):
    result = []

    po = {
        'cost': p_one.cost,
        'description': p_one.description,
        'shop': p_one.shop_id
    }

    pt = {
        'cost': p_two.cost,
        'description': p_two.description,
        'shop': p_two.shop_id
    }

    result.append(po)
    result.append(pt)

    return result


def log(msg):
    logging.log(logging.INFO, msg)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, Question):
        return obj.__dict__
    elif isinstance(obj, Comment):
        return obj.__dict__
    elif isinstance(obj, Category):
        return obj.__dict__
    elif isinstance(obj, User):
        return obj.__dict__
    elif isinstance(obj, Question_cat):
        return obj.__dict__
    raise TypeError("Type %s not serializable" % type(obj))


def get_json(source, name, default_value):
    value = None
    try:
        value = source[name]
    except:
        value = default_value
    return value


def telephone(tel):
    pattern = r'(\+7|8|7).*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2})'
    result = re.findall(pattern, tel)
    phone = ''
    z = 0
    for r in result[0]:
        if z != 0:
            phone += r
        z += 1
    return phone


def get_hash(str):
    hash_object = hashlib.md5(str.encode('utf-8'))
    return hash_object.hexdigest()





