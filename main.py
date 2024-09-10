from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List


app = FastAPI()


# Single file upload
@app.post("/uploadfiles")
async def endpoint(uploaded_file: UploadFile):
    print(uploaded_file.file)
    print(uploaded_file._in_memory)
    content = await uploaded_file.read()
    print(content)
    

#Multiplefile upload
@app.post("/uploadfiles/")
async def Upload_files(files: List[UploadFile] = File(...)):
    file_info = []
    for file in files:
        contents = await file.read()
        file_info.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(contents)    
        })
        return file_info
        
        
        
#File validation
@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ("text/csv", "application/json"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV or JSON files are allowed.")
    return {"filename": file.filename, "content_type": file.content_type}
        
        
        
 #CHECK THE SIZE
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File is too large. Maximum size is 10 MB.")
    # Process file further
    return {"filename": file.filename, "content_type": file.content_type, "size": len(contents)}
       


