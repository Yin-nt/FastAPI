from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
pymysql.install_as_MySQLdb()

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://Yin:Yen1422004@localhost/db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#tạo sự phụ thuộc (tạo 1 SQLAlchemy mới vs 1 yêu cầu duy nhất và đóng lại khi hoàn tất)
def get_db():
    db = SessionLocal()
    try: # đảm bảo session luôn đóng ngay cả khi có ngoại lệ
        yield db
    finally:
        db.close()