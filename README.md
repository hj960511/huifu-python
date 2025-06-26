# Huifu 框架 

## 介绍
Huifu 框架是一个基于python3.7，Fask的简易web框架，能够帮助你快速构建一个web应用，同时其可自动生成数据库表，无需手动创建。

## 结构目录

Huifu
 ├── base
 │   ├── cache_base.py
 │   ├── model_base.py
 ├── blue
 │   ├── api
 │   │   ├── api_cache.py
 │   │   ├── api_upload.py
 │   │   ├── api_users.py
 │   ├── web
 │   │   ├── web_cache.py
 │   │   ├── web_home.py
 │   │   ├── web_upload.py
 │   │   ├── web_user.py
 ├── cfg.py
 ├── core
 │   ├── cache_core.py
 │   ├── inh
 │   │   ├── cache_file_core_inh.py
 │   │   ├── cache_redis_core_inh.py
 │   ├── mysql_core.py
 │   ├── redis_core.py
 │   ├── upload_core.py
 ├── model
 │   ├── readme.md
 │   ├── test.py
 │   ├── upload.py
 │   ├── user.py
 ├── public
 │   ├── static
 │   │   └── index.html
 │   ├── templates
 │   │   ├── cache.html
 │   │   ├── home.html
 │   │   ├── upload.html
 │   │   └── user.html
 │   └── uploads
 ├── readme.md
 ├── requirements.txt
 ├── run.py
 ├── runing
 │   ├── cache
 │   │   └── data
 │   ├── logs
 │   └── readme.md
 ├── utils
 │   └── helper_utils.py


# 命令：

1. 导出依赖 ```pip freeze > requirements.txt```
2. 安装依赖 ```pip install -r requirements.txt```

# 部署：

## 裸跑执行：
### 步骤一、 导出：
1. 根据环境，生成``` requirements.txt ```文件
2. 在目标目录，安装依赖包

### 步骤二、 运行：
```
python app.py --env dev
python app.py --env test
python app.py --env prod
```

