import time
import uuid

from PIL import Image
import os


def generate_uuid_high_precision(filename: str) -> str:
    """根据文件名 + 当前毫秒级时间戳生成 UUID"""
    namespace = uuid.NAMESPACE_DNS
    timestamp = str(int(time.time() * 1000))  # 毫秒级时间戳
    unique_string = f"{filename}_{timestamp}"
    return str(uuid.uuid5(namespace, unique_string))


def get_image_info(image_path: str):
    """获取图片的文件大小（字节）和尺寸（像素）"""
    if not os.path.exists(image_path):
        return {"error": "文件不存在"}

    # 获取文件大小（字节）
    file_size = os.path.getsize(image_path)  # 无单位，单位为字节（Bytes）

    # 获取图片尺寸（像素）
    with Image.open(image_path) as img:
        width, height = img.size  # 图片尺寸（宽 x 高）

    return {
        "file_size": file_size,  # 文件大小（字节）
        "dimensions": f"{width}x{height}"  # 尺寸格式化输出
    }
