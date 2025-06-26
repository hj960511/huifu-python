from flask import jsonify, Blueprint, render_template

web_upload_bp = Blueprint('web_upload', __name__)


@web_upload_bp.route('/', methods=['GET'])
def index():
    return render_template("upload.html")