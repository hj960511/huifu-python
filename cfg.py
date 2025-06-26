import os
import urllib

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # 基础通用配置 默认的 运行的时候可以修改
    ENV = 'dev'
    # 调试配置
    DEBUG = False
    LOG_LEVEL = 'DEBUG'

    # 运行配置
    HOST = '127.0.0.1'
    PORT = 5000
    DOMAIN = 'localhost'
    SECRET_KEY = 'your-secret-key-here'

    # 默认目录置部分
    BASE_DIR = BASE_DIR
    TEMPLATE_FOLDER = os.path.join(BASE_DIR,  'public', 'templates')
    STATIC_FOLDER = os.path.join(BASE_DIR, 'public', 'static')
    LOG_DIR = os.path.join(BASE_DIR, 'runing','logs')

    # 运行时缓存目录
    RUNTIME_CACHE_DIR = os.path.join(BASE_DIR,  'runing', 'cache')
    # 缓存引擎 redis file两种
    CACHE_TYPE = 'file'
    # 缓存时效默认 单位 s
    CACHE_DEFAULT_TIMEOUT = 300
    # 缓存文件或key前缀
    CACHE_KEY_PREFIX = 'cache_'

    # 文件上传
    UPLOAD_FOLDER = os.path.join(BASE_DIR,  'public', 'uploads')
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # 路由配置
    BLUEPRINT_CONFIG = {
        # api_bp
        'api_cache': {
            'module': 'blue.api.api_cache',  # 蓝图模块路径
            'url_prefix': '/api/'  # 蓝图的 URL 前缀
        },
        'api_users': {
            'module': 'blue.api.api_users',  # 蓝图模块路径
            'url_prefix': '/api_users'  # 蓝图的 URL 前缀
        },
        'api_upload': {
            'module': 'blue.api.api_upload',  # 蓝图模块路径
            'url_prefix': '/api_upload'  # 蓝图的 URL 前缀
        },
        'web_home': {
            'module': 'blue.web.web_home',  # 假设你创建了一个 web.index 模块
            'url_prefix': '/'
        },
        'web_cache': {
            'module': 'blue.web.web_cache',  # 假设你创建了一个 web.index 模块
            'url_prefix': '/cache'
        },
        'web_user': {
            'module': 'blue.web.web_user',  # 假设你创建了一个 web.index 模块
            'url_prefix': '/user'
        },
        'web_upload': {
            'module': 'blue.web.web_upload',  # 假设你创建了一个 web.index 模块
            'url_prefix': '/upload'
        },
    }


class DevConfig(Config):
    DEBUG = True
    # mysql配置 localhost  3306 root 注意密码不可存在@符号 test utf-8
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:admin888@localhost:3306/test?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # redis配置
    REDIS_CONFIG = {
        'CACHE_REDIS_HOST': 'localhost',
        'CACHE_REDIS_PORT': 6379,
        'CACHE_REDIS_PASSWORD': None,
        'CACHE_REDIS_DB': 0
    }


class TestConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False
