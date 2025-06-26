import importlib
import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import create_engine, inspect, MetaData
from sqlalchemy.exc import SQLAlchemyError
from cfg import Config

db = SQLAlchemy()


class MysqlClient:
    """
    Mysql 数据库连接类
    """

    def __init__(self):
        self.mysql_client = None

    def run(self, app: Flask):
        db.init_app(app)
        self.import_all_models()

        with app.app_context():
            try:
                # 尝试连接数据库
                engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
                conn = engine.connect()
                print("✅ 数据库连接成功！")

                inspector = inspect(engine)

                metadata = MetaData()
                metadata.reflect(bind=engine)

                # 获取当前所有表名
                existing_tables = inspector.get_table_names()

                with db.engine.begin() as connection:
                    for table in db.metadata.tables.values():
                        if table.name not in existing_tables:
                            print(f"⚙️ 正在创建缺失的表：{table.name}")
                            table.create(bind=connection)
                        else:
                            print(f"✅ 表已存在：{table.name}")

                conn.close()

            except SQLAlchemyError as e:
                print(f"❌ 数据库连接失败: {str(e)}")

    def import_all_models(self):
        # 获取当前 model 目录
        model_dir = os.path.join(Config.BASE_DIR, 'model')

        for filename in os.listdir(model_dir):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = f'model.{filename[:-3]}'
                try:
                    importlib.import_module(module_name)
                    print(f"✅ 已导入模型：{module_name}")
                except Exception as e:
                    print(f"❌ 导入模型失败：{e}")


mysql_client = MysqlClient()
