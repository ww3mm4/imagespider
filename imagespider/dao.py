from sqlalchemy import Column, String,Integer
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True,nullable=True,autoincrement=True)
    img_url = Column(String(2083),nullable=False)
    title = Column(String(2083),nullable=False)