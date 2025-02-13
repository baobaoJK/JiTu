from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Pic(Base):
    __tablename__ = 'pic_list'

    pid = Column(Integer, primary_key=True)
    uuid = Column(String)
    pic_path = Column(String)
    pic_name = Column(String)
    pic_original_name = Column(String)
    pic_file_size = Column(BigInteger)
    pic_type = Column(String)
    pic_size = Column(String)
    pic_suffix = Column(String)
    upload_time = Column(DateTime)

    def to_dict(self):
        return {
            'pid': self.pid,
            'uuid': self.uuid,
            'pidPath': self.pic_path,
            'picName': self.pic_name,
            'picOriginalName': self.pic_original_name,
            'picFileSize': self.pic_file_size,
            'picType': self.pic_type,
            'picSize': self.pic_size,
            'picSuffix': self.pic_suffix,
            'uploadTime': str(self.upload_time)
        }
