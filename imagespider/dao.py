from sqlalchemy import Column, String,Integer
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True,autoincrement=True)
    img_url = Column(String(1024),nullable=False,unique=True)
    title = Column(String(1024),nullable=False)