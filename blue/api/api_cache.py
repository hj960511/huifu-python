# blue/api_cache.py

from flask import Blueprint, jsonify, request
from flask import current_app  # 获取当前 app 实例

api_cache_bp = Blueprint('api_cache', __name__)

@api_cache_bp.route('/cache/set', methods=['POST'])
def set_cache():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    ttl = data.get('ttl', None)
    if isinstance(ttl, str):
        try:
            ttl = float(ttl)
        except ValueError:
            raise ValueError("ttl 字符串无法转换为数字")

    if not key or value is None:
        return jsonify({"error": "缺少 key 或 value"}), 400

    current_app.cc_local.set(key, value, ttl)
    return jsonify({"message": f"缓存 {key} 已设置", "key": key, "value": value})


@api_cache_bp.route('/cache/get/<key>', methods=['GET'])
def get_cache(key):
    value = current_app.cc_local.get(key)
    if value is None:
        return jsonify({"error": "缓存不存在或已过期"}), 404
    return jsonify({"key": key, "value": value})


@api_cache_bp.route('/cache/delete/<key>', methods=['DELETE'])
def delete_cache(key):
    if current_app.cc_local.exists(key):
        current_app.cc_local.delete(key)
        return jsonify({"message": f"缓存 {key} 已删除"})
    else:
        return jsonify({"error": "缓存不存在"}), 404

