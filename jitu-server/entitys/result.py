from flask import jsonify


class Result:
    """统一 API 响应格式"""
    def __init__(self, message="成功", status=200, data=None):
        self.message = message  # 提示信息
        self.status = status  # HTTP 状态码
        self.data = data if data is not None else None

    def set_error(self, message, status=400):
        """快速设置错误信息"""
        self.message = message
        self.status = status
        return self  # 方便链式调用

    def to_dict(self):
        """返回 JSON 格式"""
        data = {
            "status": self.status,
            "message": self.message,
        }

        if self.data is not None:
            data['data'] = self.data

        return jsonify(data), self.status
