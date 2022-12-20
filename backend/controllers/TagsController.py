from backend.entities.Category import Category
from flask import Blueprint, request
from backend.utils import Utils


tags = Blueprint('tags', __name__)


@tags.route('/api/tags/search', methods=['POST'])
def api_tags_search():
    request_data = request.get_json()
    name = request_data['name'].strip()
    tags = request_data['tags']
    categories = []
    category = Category.query.filter(Category.title.contains(name)).order_by(Category.id.desc()).all()
    for cat in category:
        if cat.id in tags:
            continue
        else:
            categories.append(cat.as_dict())
    return Utils.getAnswer({'tags': categories})