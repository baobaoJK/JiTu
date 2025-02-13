# 创建 Blueprint，指定 url_prefix="/api"
import os

from flask import Blueprint, request

from entitys.result import Result
from entitys.sql.pic import Pic
from utils import get_upload_folder
from utils.sql_connect import get_sql_session

pic_bp = Blueprint("pic", __name__, url_prefix="/api")


# 获取图片数量
@pic_bp.route('/getPicCount', methods=['GET'])
def get_pic_count():
    result = Result()

    sql_session = get_sql_session()
    pic_count = sql_session.query(Pic).count()
    result.data = {
        "picCount": pic_count
    }
    sql_session.close()

    return result.to_dict()


# 获取图片列表
@pic_bp.route('/getPicList', methods=['GET'])
def get_images():
    """获取图片列表，支持分页和相册筛选"""
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("perPage", default=10, type=int)
    album = request.args.get("album", default="默认相册", type=str)  # 查询相册

    # 查询数据库
    sql_session = get_sql_session()
    query = sql_session.query(Pic).filter(Pic.pic_path == album)
    total = query.count()
    images = query.order_by(Pic.upload_time.desc()).offset((page - 1) * per_page).limit(per_page).all()

    # 获取本机地址
    local_url = request.host_url
    BASE_IMAGE_URL = local_url + "/api/files"

    # 构造响应数据
    image_list = []
    for img in images:
        if img.pic_path == '默认相册':
            image_url = f"{BASE_IMAGE_URL}/{img.uuid}{img.pic_suffix}"
        else:
            image_url = f"{BASE_IMAGE_URL}/{img.pic_path}/{img.uuid}{img.pic_suffix}"
        image_list.append({
            "pid": img.pid,
            "uuid": img.uuid,
            "picPath": img.pic_path,
            "url": image_url,
            "picName": img.pic_name,
            "picOriginalName": img.pic_original_name,
            "picFileSize": img.pic_file_size,
            "picType": img.pic_type,
            "picSize": img.pic_size,
            "uploadTime": img.upload_time.strftime("%Y-%m-%d %H:%M:%S"),
        })
    result = Result()
    result.data = {
        "page": page,
        "perPage": per_page,
        "total": total,
        "images": image_list
    }

    return result.to_dict()


# 移动图片
@pic_bp.route('/pic', methods=['POST'])
def move_pic():
    result = Result()

    pid_list = request.json.get('pidList')
    pic_path = request.json.get('picPath')

    if not pid_list or not pic_path:
        result.set_error('错误')
        result.data = {
            "message": "参数错误"
        }
        return result.to_dict()

    upload_folder = get_upload_folder()
    target_path = os.path.join(upload_folder, pic_path)

    if not os.path.exists(target_path) and pic_path != '默认相册':
        result.set_error('错误')
        result.data = {
            "message": "路径不存在"
        }
        return result.to_dict()

    try:
        sql_session = get_sql_session()

        for pid in pid_list:
            pic = sql_session.query(Pic).filter(Pic.pid == pid).first()

            if pic_path == '默认相册':
                old_path = os.path.join(upload_folder, pic.pic_path + '\\' + pic.uuid + pic.pic_suffix)
                new_path = os.path.join(upload_folder, pic.uuid + pic.pic_suffix)
            elif pic.pic_path == '默认相册':
                old_path = os.path.join(upload_folder, pic.uuid + pic.pic_suffix)
                new_path = os.path.join(upload_folder, pic_path + '\\' + pic.uuid + pic.pic_suffix)
            else:
                old_path = os.path.join(upload_folder, pic.pic_path + '\\' + pic.uuid + pic.pic_suffix)
                new_path = os.path.join(upload_folder, pic_path + '\\' + pic.uuid + pic.pic_suffix)

            os.rename(old_path, new_path)
            pic.pic_path = pic_path
            sql_session.commit()
            sql_session.close()

        result.data = {
            "message": f"移动到 {pic_path} 相册成功"
        }
    except Exception as e:
        result.set_error('错误')
        result.data = {
            "message": "移动失败"
        }
        print(e)

    return result.to_dict()


# 重命名图片
@pic_bp.route('/pic', methods=['PUT'])
def rename_pic():
    result = Result()

    pid = request.json.get('pid')
    rename = request.json.get('rename')

    if not pid or not rename:
        result.set_error('错误')
        result.data = {
            "message": "参数错误"
        }
        return result

    sql_session = get_sql_session()
    pic = sql_session.query(Pic).filter(Pic.pid == pid).first()
    if pic:
        pic.pic_name = rename
        sql_session.commit()
        sql_session.close()
        result.data = {
            "message": "重命名成功"
        }
    else:
        result.set_error('错误')
        result.data = {
            "message": "图片不存在"
        }
    return result.to_dict()


# 删除图片
@pic_bp.route('/pic', methods=['DELETE'])
def delete_pic():
    result = Result()

    delete_pic_list = request.json.get('deletePicList')

    if not delete_pic_list:
        result.set_error('错误')
        result.data = {
            'message': '删除列表为空'
        }
        return result

    upload_folder = get_upload_folder()

    sql_session = get_sql_session()

    for pid in delete_pic_list:
        img = sql_session.query(Pic).filter(Pic.pid == pid).first()
        # 文件删除
        if img and img.pic_path != '默认相册':
            target_folder = os.path.join(upload_folder, img.pic_path)
        else:
            target_folder = os.path.join(upload_folder)

        url = (target_folder + '//' + img.uuid + img.pic_suffix)
        os.remove(url)
        # 数据库删除
        sql_session.delete(img)

    sql_session.commit()
    sql_session.close()

    result.data = {
        'message': '删除成功',
    }
    return result.to_dict()
