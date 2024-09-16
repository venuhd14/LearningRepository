from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()
MAX_FILE_SIZE = 100 * 1024 * 1024
VALID_EXTENSION = {'image/jpeg','text/csv'}

@app.post("/upload")
async def Upload_file(file: UploadFile = File(...)):
    if file.content_type not in VALID_EXTENSION:
        raise HTTPException(status_code=400, detail="Invalid file type. Only Jpeg & csv files are allowed.")
    contents = await file.read()
    
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File is too large. Maximum size is 100 MB.") 

    return {
        "filename": file.filename,
        "content_type":file.content_type,
        "size": len(contents)
    }

