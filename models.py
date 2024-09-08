from sqlalchemy import Column, Integer, String,TIMESTAMP
from sqlalchemy.types import String
from database import Base
import datetime

class File(Base):
    __tablename__ = "files_metadata"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String,index=True)
    original_filename = Column(String)
    file_path = Column(String, index=True)
    file_size = Column(Integer)
    created_at = Column(TIMESTAMP,default=datetime.datetime.now)