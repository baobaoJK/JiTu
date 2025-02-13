import os
import shutil
from datetime import datetime

from flask import Blueprint, request
from sqlalchemy import func

from entitys.result import Result
from entitys.sql.pic import Pic
from entitys.sql.pic_folder import PicFolder
from utils import get_upload_folder
from utils.sql_connect import get_sql_session

folder_bp = Blueprint("folder", __name__, url_prefix="/api")


# 创建相册
@folder_bp.route("/picFolder", methods=["POST"])
def addPicFolder():
    folder_name = request.json.get("folderName")

    result = Result()
    if not folder_name:
        result.set_error("错误")
        result.data = {
            "message": "请输入文件夹名称"
        }
        return result.to_dict()

    try:
        upload_folder = get_upload_folder()
        target_folder = os.path.join(upload_folder, folder_name)

        if os.path.exists(target_folder):
            result.set_error("文件夹已存在")
            return result.to_dict()

        os.mkdir(target_folder)

        sql_session = get_sql_session()

        pic_list = PicFolder()
        pic_list.pic_folder_name = folder_name
        pic_list.create_time = datetime.now()
        sql_session.add(pic_list)
        sql_session.commit()
        sql_session.close()

        result.data = {
            'message': "添加成功"
        }
    except Exception as e:
        result.set_error("添加失败")

    return result.to_dict()


# 获取相册列表
@folder_bp.route("/picFolder", methods=["GET"])
def getPicFolderList():
    result = Result()

    sql_session = get_sql_session()
    # 使用 SQLAlchemy 查询 pic_folder_list 表的 pic_folder_name 和 pic_list 表的每个 pic_path 的图片数量
    pic_folder_list = (
        sql_session.query(
            PicFolder.pid,
            PicFolder.pic_folder_name,
            func.count(Pic.pic_path).label('group_count')
        )
        .join(Pic, Pic.pic_path == PicFolder.pic_folder_name, isouter=True)  # 外连接，匹配 pic_folder_name 和 pic_path
        .group_by(PicFolder.pid, PicFolder.pic_folder_name)  # 按照 pic_folder_name 分组
        .order_by(PicFolder.pid)
        .all()
    )

    # 关闭 SQLAlchemy 会话
    sql_session.close()

    # 将查询结果转换为字典列表
    result.data = {
        'picFolderList': [{'pid': folder[0], 'picFolderName': folder[1], 'picCount': folder[2]} for folder in pic_folder_list]
    }

    return result.to_dict()


# 修改相册名称
@folder_bp.route("/picFolder", methods=["PUT"])
def updatePicFolderName():
    result = Result()

    try:
        rename = request.json.get('rename')
        pid = request.json.get("folderId")
        folder_name = request.json.get("folderName")

        upload_folder = get_upload_folder()
        target_folder = os.path.join(upload_folder, rename)

        if os.path.exists(target_folder):
            result.set_error("文件夹已存在")
            return result.to_dict()

        # 修改文件夹名字
        os.rename(os.path.join(upload_folder, folder_name), target_folder)

        sql_session = get_sql_session()

        pic_folder = sql_session.query(PicFolder).filter(PicFolder.pid == pid).first()
        pic_folder.pic_folder_name = rename

        # 修改图片路径
        pic_list = sql_session.query(Pic).filter(Pic.pic_path == folder_name).all()

        for pic in pic_list:
            pic.pic_path = rename

        sql_session.commit()
        sql_session.close()

        result.data = {
            'message': "修改成功"
        }
    except Exception as e:
        print(e)
        result.set_error("修改失败")
    return result.to_dict()


# 删除相册
@folder_bp.route("/picFolder", methods=["DELETE"])
def deletePicFolder():
    result = Result()

    try:
        folder_id = request.json.get("folderId")
        folder_name = request.json.get("folderName")
        upload_folder = get_upload_folder()
        target_folder = os.path.join(upload_folder, folder_name)

        if os.path.exists(target_folder):
            shutil.rmtree(target_folder)

        sql_session = get_sql_session()

        pic_folder = sql_session.query(PicFolder).filter(PicFolder.pid == folder_id).first()
        sql_session.delete(pic_folder)

        pic_sql_list = sql_session.query(Pic).filter(Pic.pic_path == folder_name).all()

        if pic_sql_list is not None:
            for pic in pic_sql_list:
                sql_session.delete(pic)

        sql_session.commit()
        sql_session.close()

        result.data = {
            'message': "删除成功"
        }
    except Exception as e:
        print(e)
        result.set_error("删除失败")
    return result.to_dict()
