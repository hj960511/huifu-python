from flask import jsonify, Blueprint, render_template

web_user_bp = Blueprint('web_user', __name__)


@web_user_bp.route('/', methods=['GET'])
def index():
    return render_template("user.html")