from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List
app = FastAPI()

# Constants for file validation
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_CONTENT_TYPES = {"text/csv", "application/json"}

# Single file upload
@app.post("/uploadfile/single")
async def upload_single_file(uploaded_file: UploadFile = File(...)):
    if uploaded_file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV or JSON files are allowed.")
    
    contents = await uploaded_file.read()
    
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File is too large. Maximum size is 10 MB.")
    
    return {
        "filename": uploaded_file.filename,
        "content_type": uploaded_file.content_type,
        "size": len(contents)
    }

# Multiple file upload
@app.post("/uploadfile/multiple")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    file_info = []
    
    for file in files:
        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(status_code=400, detail=f"Invalid file type for {file.filename}. Only CSV or JSON files are allowed.")
        
        contents = await file.read()
        
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"File {file.filename} is too large. Maximum size is 10 MB.")
        
        file_info.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(contents)
        })
    
    return file_info

# File validation for type
@app.post("/uploadfile/validate")
async def validate_file(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV or JSON files are allowed.")
    
    contents = await file.read()
    
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File is too large. Maximum size is 10 MB.")
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }

