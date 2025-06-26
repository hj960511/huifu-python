# blue/api/api_upload.py
from flask import Blueprint, request, jsonify
from core.upload_core import handle_file_upload, handle_file_download, handle_file_delete
from model.upload import Upload

api_upload_bp = Blueprint('api_upload', __name__, url_prefix='/api_upload')


@api_upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '未找到文件'})
    file = request.files['file']
    result = handle_file_upload(file)
    return jsonify(result)


@api_upload_bp.route('/uploads', methods=['GET'])
def get_upload_list():
    """获取上传列表 根据数据库"""
    uploads = Upload.query.all()
    result = [
        {
            'id': upload.id,
            'filename': upload.filename,
            'file_type': upload.file_type,
            'size': upload.size,
            'md5': upload.md5,
            'upload_time': upload.upload_time.isoformat() if upload.upload_time else None,
            'absolute_path': upload.absolute_path,
            'unique_filename': upload.unique_filename
        }
        for upload in uploads
    ]
    return jsonify(result)


@api_upload_bp.route('/download/<md5>', methods=['GET'])
def download_file(md5):
    return handle_file_download(md5)


@api_upload_bp.route('/delete/<md5>', methods=['DELETE'])
def delete_file(md5):
    result = handle_file_delete(md5)
    return jsonify(result)
