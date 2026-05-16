from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# CloudBase MySQL 环境变量（自动注入）
MYSQL_HOST = os.getenv("TCB_MYSQL_HOST")
MYSQL_PORT = os.getenv("TCB_MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("TCB_MYSQL_USER")
MYSQL_PASSWORD = os.getenv("TCB_MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("TCB_MYSQL_DATABASE")

# 本地 SQLite 备用
LOCAL_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./game_guide.db")

# 判断使用 MySQL 还是 SQLite
if MYSQL_HOST and MYSQL_USER and MYSQL_PASSWORD and MYSQL_DATABASE:
    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"
    print(f"[数据库] 使用 CloudBase MySQL: {MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")
else:
    DATABASE_URL = LOCAL_DATABASE_URL
    print(f"[数据库] 使用本地 SQLite: {DATABASE_URL}")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
