import os
from datetime import datetime

from flask import Blueprint, request, send_from_directory, abort
from werkzeug.utils import secure_filename

from entitys.result import Result
from entitys.sql.pic import Pic
from utils import get_upload_folder
from utils.sql_connect import get_sql_session
from utils.utils import generate_uuid_high_precision, get_image_info

# 创建 Blueprint，指定 url_prefix="/api"
upload_bp = Blueprint("upload", __name__, url_prefix="/api")

# 读取配置，设置上传文件保存目录
upload_folder = get_upload_folder()
os.makedirs(upload_folder, exist_ok=True)  # 确保上传目录存在

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route("/upload", methods=["POST"])
def handle_upload():
    result = Result()
    """处理文件上传"""
    if "file" not in request.files:
        return result.set_error('没有文件').to_dict()

    file = request.files["file"]

    if file.filename == "":
        return result.set_error('未选择文件').to_dict()

    if not allowed_file(file.filename):
        return result.set_error('文件类型不允许').to_dict()

    # 生成安全的文件名
    origin_filename = file.filename
    filename = secure_filename(file.filename)

    # 获取用户选择的子目录
    subdir = request.form.get("subdir", "").strip()

    # 构造最终保存目录
    save_folder = os.path.join(upload_folder, subdir) if subdir else upload_folder
    os.makedirs(save_folder, exist_ok=True)  # 确保目录存在

    # 更改文件名称
    file_uuid = generate_uuid_high_precision(filename)
    file_suffix = os.path.splitext(filename)[1]
    filename = file_uuid + file_suffix

    # 保存文件
    file_path = os.path.join(save_folder, filename)
    file.save(file_path)

    # 图片信息
    img_info = get_image_info(file_path)

    # 数据库操作
    session = get_sql_session()
    pic = Pic()
    pic.uuid = file_uuid
    pic.pic_path = '默认相册'
    pic.pic_name = origin_filename
    pic.pic_original_name = origin_filename
    pic.pic_file_size = img_info['file_size']
    pic.pic_type = file.content_type
    pic.pic_size = img_info['dimensions']
    pic.pic_suffix = file_suffix
    pic.upload_time = datetime.now()

    session.add(pic)
    session.commit()

    # 返回成功信息
    result.message = '图片上传成功'
    result.data = {
        'filename': filename,
    }
    return result.to_dict()


@upload_bp.route("/files/<path:filepath>")
def serve_file(filepath):
    """提供文件访问支持 N 个子目录"""
    full_path = os.path.join(upload_folder, filepath)

    # 防止目录遍历攻击，确保访问在 UPLOAD_FOLDER 内部
    if not os.path.abspath(full_path).startswith(os.path.abspath(upload_folder)):
        abort(403)

    # 分离目录和文件名
    directory = os.path.dirname(full_path)
    filename = os.path.basename(full_path)

    if not os.path.exists(full_path):
        abort(404)

    return send_from_directory(directory, filename)
