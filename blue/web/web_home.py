from flask import jsonify, Blueprint, render_template

web_home_bp = Blueprint('web_home', __name__)

@web_home_bp.route('/', methods=['GET'])
def index():
    data = {
        "message": "欢迎来到Huifu，一个简洁的开发框架！",
        # 示例：修改 items 数据结构以包含 name 和 url
        "items": [
            {"name": "缓存", "url": "/cache"},
            {"name": "用户", "url": "/user"},
            {"name": "文件上传", "url": "/upload"},
        ]
    }
    return render_template('home.html', **data)


