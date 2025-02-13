from flask import Blueprint, request

from entitys.result import Result
from utils import load_config, save_config

system_bp = Blueprint("system", __name__, url_prefix="/api")

config = load_config()


# 获取应用配置
@system_bp.route("/getConfig", methods=["GET"])
def get_config():
    result = Result()
    result.data = config
    return result.to_dict()


# 设置应用名称
@system_bp.route("/setConfig", methods=["PUT"])
def set_config():
    # 获取前端传过来的值
    name = request.json.get('name')

    result = Result()

    # 判断是否为空
    if not name:
        result.set_error('请输入需要修改的名称')
        return result.to_dict()

    # 修改配置文件
    config['server']['name'] = name
    save_config(config)

    # 返回结果
    result.data = {
        'name': name,
        'message': '修改成功'
    }
    return result.to_dict()
