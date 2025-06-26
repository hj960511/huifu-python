import os
import importlib
import logging
import sys
from datetime import datetime

from flask import Flask
from cfg import Config, DevConfig, TestConfig, ProdConfig
from core.mysql_core import mysql_client
from core.redis_core import redis_client
from core.cache_core import cc_local

def register_blueprints(app: Flask, BLUEPRINT_CONFIG=None):
    """
    根据配置文件中的定义动态注册所有蓝图
    """
    for blueprint_name, config in BLUEPRINT_CONFIG.items():
        module_path = config['module']
        url_prefix = config.get('url_prefix', None)

        try:
            # 动态导入模块
            module = importlib.import_module(module_path)
            blueprint = getattr(module, f"{blueprint_name}_bp")

            if blueprint:
                app.register_blueprint(blueprint, url_prefix=url_prefix)
                print(f"✅ 已注册蓝图：{blueprint_name} -> {module_path} (URL前缀: {url_prefix})")
            else:
                raise AttributeError(f"未找到蓝图对象 {blueprint_name}_bp 在模块 {module_path}")
        except Exception as e:
            print(f"❌ 注册蓝图失败：{e}")


# 根据环境变量选择配置
def get_config(env = None):
    # env 为空 则使用默认环境变量
    if not env:
        env = Config.ENV
    if env == 'dev':
        print("当前配置：开发环境配置")
        return DevConfig
    elif env == 'test':
        print("当前配置：测试环境配置")
        return TestConfig
    elif env == 'prod':
        print("当前配置：生产环境配置")
        return ProdConfig
    else:
        raise ValueError(f"错误配置项，请检查: {env}")


def configure_logging():
    # 创建日志目录（如果不存在）
    os.makedirs(Config.LOG_DIR, exist_ok=True)

    # 按照当前日期生成日志文件名：logs/2025-04-05.log
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(Config.LOG_DIR, f'{today}.log')

    # 配置 logging 模块
    logging.basicConfig(
        level=Config.LOG_LEVEL,
        filename=log_file,
        filemode='a',
        encoding='utf-8',  # 添加这一行，明确指定编码格式
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 获取 root logger 并添加 StreamHandler 以支持 stdout/stderr 捕获
    logger = logging.getLogger()
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(Config.LOG_LEVEL)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 替换 sys.stdout/sys.stderr 为实时写入的日志流
    class LoggingWriter:
        def __init__(self, level):
            self.level = level

        def write(self, message):
            if message.strip():  # 忽略空行
                self.level(message.rstrip())

        def flush(self):  # 确保实时刷新
            pass

    sys.stdout = LoggingWriter(logging.info)
    sys.stderr = LoggingWriter(logging.error)

    # 记录应用启动信息
    logging.info('Huifu 运行成功')


def create_app(config_name='dev'):
    config = get_config(config_name)
    app = Flask(__name__,
                template_folder=config.TEMPLATE_FOLDER,
                static_folder=config.STATIC_FOLDER)
    app.config.from_object(config)
    configure_logging()
    mysql_client.run(app)
    redis_client.run(app)
    cc_local.run(app)

    # 确保在注册蓝图之前推送应用上下文
    with app.app_context():
        register_blueprints(app, config.BLUEPRINT_CONFIG)

    return app


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run the app with a specified environment.")
    parser.add_argument('--env', choices=['dev', 'test', 'prod'], default='dev',
                        help='The environment to run the app in (default: dev)')
    args = parser.parse_args()

    app = create_app(config_name=args.env)

    app.run(
        debug=app.config['DEBUG'],
        use_reloader=False,
        host=app.config['HOST'],
        port=app.config['PORT']
    )


if  __name__ == '__main__':
    main()