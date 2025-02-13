from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import load_config


# 获取数据库连接
def get_sql_session():
    config = load_config()
    SQL_CONFIG = config['mysql']
    # 数据库引擎和会话创建

    SQL_USERNAME = SQL_CONFIG['username']  # 数据库用户名
    SQL_PASSWORD = SQL_CONFIG['password']  # 数据库密码
    SQL_HOST = SQL_CONFIG['host']          # 数据库地址
    SQL_PORT = SQL_CONFIG['port']          # 数据库端口
    SQL_DATABASE = SQL_CONFIG['database']  # 数据库名称

    engine = create_engine(f'mysql+pymysql://{SQL_USERNAME}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DATABASE}')
    Session = sessionmaker(bind=engine)
    sql_session = Session()

    return sql_session
