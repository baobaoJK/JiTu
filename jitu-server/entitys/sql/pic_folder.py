from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PicFolder(Base):
    __tablename__ = 'pic_folder_list'

    pid = Column(Integer, primary_key=True)
    pic_folder_name = Column(String)
    create_time = Column(DateTime)

    def to_dict(self):
        return {
            'pid': self.pid,
            'picFolderName': self.pic_folder_name,
            'createTime': str(self.create_time)
        }
