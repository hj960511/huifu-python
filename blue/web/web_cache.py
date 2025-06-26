from flask import jsonify, Blueprint, render_template

web_cache_bp = Blueprint('web_cache', __name__)


@web_cache_bp.route('/', methods=['GET'])
def index():
    return render_template("cache.html")