import os
import hashlib
import uuid
from flask import current_app, send_from_directory
from model.upload import Upload, db


def allowed_file(filename):
    """检查文件类型是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def get_file_md5(file_stream):
    """计算文件的 MD5 值"""
    md5_hash = hashlib.md5()
    for chunk in iter(lambda: file_stream.read(4096), b""):
        md5_hash.update(chunk)
    file_stream.seek(0)  # 重置文件流位置
    return md5_hash.hexdigest()


def save_upload_record(filename, file_type, size, md5, absolute_path, unique_filename):
    existing = Upload.query.filter_by(md5=md5).first()
    if not existing:
        record = Upload(
            filename=filename,
            file_type=file_type,
            size=size,
            md5=md5,
            absolute_path=absolute_path,
            unique_filename=unique_filename  # ✅ 存储唯一文件名
        )
        db.session.add(record)
        db.session.commit()
        return True
    return False



from datetime import datetime

def handle_file_upload(file):
    """处理上传逻辑"""
    if not allowed_file(file.filename):
        return {'success': False, 'message': '不允许的文件类型'}

    original_name = file.filename
    file_type = original_name.rsplit('.', 1)[1].lower() if '.' in original_name else ''
    file_size = os.fstat(file.fileno()).st_size
    file_md5 = get_file_md5(file)

    # 检查md5 判断文件是否存在 如果存在 则直接返回
    upload = Upload.query.filter_by(md5=file_md5).first()
    if  upload:
        file_name = upload.unique_filename
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)
        if os.path.exists(file_path):
            return {'success': True, 'url': upload.absolute_url}

    # 使用唯一文件名防止覆盖
    unique_filename = f"{uuid.uuid4()}_{original_name}"

    # 获取当前日期并创建目录结构（如 uploads/2025-06-11）
    today = datetime.now().strftime("%Y-%m-%d")
    upload_folder = current_app.config['UPLOAD_FOLDER']
    date_folder = os.path.join(upload_folder, today)
    os.makedirs(date_folder, exist_ok=True)

    file_path = os.path.join(date_folder, unique_filename)

    domain = current_app.config['DOMAIN']
    absolute_url = f"http://{domain}/uploads/{today}/{unique_filename}"

    if not os.path.exists(file_path):
        file.save(file_path)

    if save_upload_record(original_name, file_type, file_size, file_md5, absolute_url, unique_filename):
        return {'success': True, 'url': absolute_url}
    else:
        return {'success': False, 'message': '文件已存在'}



def handle_file_download(md5):
    """根据 MD5 处理下载逻辑"""
    record = Upload.query.filter_by(md5=md5).first()
    if not record:
        return {'success': False, 'message': '文件不存在'}, 404

    # 根据创建时间进行拼接得到
    upload_date = record.upload_time
    date_str = upload_date.strftime('%Y-%m-%d')  # 输出类似 "2025-06-11"
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], date_str)
    return send_from_directory(directory=upload_folder, path=record.unique_filename, as_attachment=True, download_name=record.filename)

def handle_file_delete(md5):
    """根据 MD5 删除文件及记录"""
    record = Upload.query.filter_by(md5=md5).first()
    if not record:
        return {'success': False, 'message': '文件不存在'}

    # 检查 unique_filename 是否存在
    if not record.unique_filename:
        return {'success': False, 'message': '无法删除：文件名缺失'}

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], record.unique_filename)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        db.session.delete(record)
        db.session.commit()
        return {'success': True}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': str(e)}


