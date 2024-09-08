from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas
from sqlalchemy import and_,text
from typing import Annotated
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os
import uuid
from utils import size_in_kb,remove_file,get_extension,update_data_helper


#This will ensure to make a folder for files storage at start of app
@asynccontextmanager
async def lifespan(app: FastAPI):
    directory = 'Files'
    if not os.path.exists(directory):
        os.makedirs(directory)
    yield


app = FastAPI(lifespan=lifespan)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def welcome():
    return {"message":"Hello World!"}


@app.post("/files/upload")
async def upload_file(file:UploadFile,db: Session = Depends(get_db)):
    try:
        file_uuid = str(uuid.uuid4())
        filename = file.filename
        file_path = f'Files/{file_uuid}_{filename}'
        with open(file_path,"wb") as buffer:
            buffer.write(await file.read())

        size_kb = size_in_kb(file_path)
        db_image = models.File(uuid=file_uuid,original_filename=filename,file_path=file_path,file_size=size_kb)
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
    except Exception as e:
        remove_file(file_path)
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return {"file":filename,"file_id":file_uuid}


@app.get("/files/{file_id}")
def read_file(file_id:str,db: Session = Depends(get_db)):
    file = db.query(models.File).filter(models.File.uuid == file_id).first()
    if file is None:
        raise HTTPException(status_code =404, detail="File not found")
    file_path = file.file_path
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        db.delete(file)
        db.commit()
    return {"message":"{file_id} does not exists!"}

@app.get("/files",response_model=list[schemas.FileResponseModel])
def list_files( skip:int =0,limit:int =10,db: Session = Depends(get_db)):
    files = db.query(models.File.uuid,models.File.original_filename,models.File.file_size,models.File.created_at,models.File.id).offset(skip).limit(limit).all()
    results = [{"uuid":row[0],"file_name":row[1],"file_size":str(row[2])+"KB","created_at":str(row[3]),"id":row[4]} for row in files]
    return results

@app.delete("/files/{file_id}")
def delete_file(file_id: str,db: Session = Depends(get_db)):
    file = db.query(models.File).filter(models.File.uuid==file_id).first()
    if file is None:
        raise HTTPException(status_code =404, detail="File not found")
    db.delete(file)
    db.commit()    
    try:
        remove_file(file.file_path)
    except Exception as e:
        db.roll_back()
        return {"Error":str(e)}
        
    return {"message":"File has been deleted successfully!"}

#We can either upload a new file or update name of previously uploaded file
@app.put("/files/{file_id}")
async def update_file(file_id: str,new_filename: Annotated[str|None, Form()]=None,file: UploadFile | None = None,db: Session = Depends(get_db)):
    try:
        current_file =  db.query(models.File).filter(models.File.uuid==file_id).first()
        if current_file is None:
            raise HTTPException(status_code =404, detail="File not found")
        
        current_file_path = current_file.file_path
        if file:
            filename = file.filename
            file_path = f'Files/{current_file.uuid}_{filename}'
            os.remove(current_file_path)
            with open(file_path,"wb") as buffer:
                buffer.write(await file.read())
            
            size_kb = size_in_kb(file_path)
            update_data_helper(current_file,filename,file_path,size_kb)

        elif new_filename:
            extension = get_extension(current_file.original_filename)
            complete_new_filename = new_filename+"."+extension
            new_path = f'Files/{file_id}_{new_filename}.{extension}'
            previous_name = current_file.original_filename
            os.rename(current_file.file_path,new_path)
            size_kb = size_in_kb(new_path)
            update_data_helper(current_file,complete_new_filename,new_path,size_kb)

        else:
            raise HTTPException(status_code=400, detail="No file or new filename provided")
    
    except FileNotFoundError as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=f"File not found: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to rename file: {str(e)}")


    db.commit()
    db.refresh(current_file) 
    return {"message":"File has been Updated successfully!"}

