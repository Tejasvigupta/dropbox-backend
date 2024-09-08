from pydantic import BaseModel
from datetime import datetime

class FileResponseModel(BaseModel):
    uuid:str
    file_name:str
    file_size:str
    created_at:datetime
    id:int


    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')  # Custom format without 'T'
        }
