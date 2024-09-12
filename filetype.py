from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List
# from fastapi.responses import JSONResponse 
import pandas as pd
import magic
import os

app = FastAPI()

# VALID_EXTENSION = {'.jpeg', '.png', '.csv', '.txt', '.pdf'}

# def get_file_extension(filename: str) ->str:
#     return os.path.splitext(filename)[1].lower()

# #file extension
# @app.post("/upload")
# async def upload_file(file: UploadFile=File(...)):
#     file_extension = get_file_extension(file.filename)
#     if file_extension not in VALID_EXTENSION:
#         raise HTTPException(status_code=400, detail = "invalid file extension")
#     return {"filename": file.filename, "extension": file_extension}


# # MIME type detection function
# def get_mime_type(file: UploadFile) -> str:
#     mime = magic.Magic()
#     # Read the first chunk of the file to determine its MIME type
#     file_content = file.file.read(1024)  # Read first 1024 bytes
#     file.file.seek(0)  # Reset file pointer
#     return mime.from_buffer(file_content)

# @app.post("/upload")
# async def upload_image(file: UploadFile=File(...)):
#     valid_mime_type = {'application/pdf', 'image/jpeg', 'image/png'}
    
#     mime_type = get_mime_type(file)
#     if mime_type not in valid_mime_type:
#         raise HTTPException(status_code=400, detail = "invalid file type")
#     # file_extension = get_file_extension(file.filename)
#     # if file_extension not in VALID_EXTENSION:
#     #     raise HTTPException(status_code=400, detail = "invalid file extension")
#     return {"filename": file.filename, "mime_type": mime_type}



#  PDF signature
def is_pdf_file(file: UploadFile) -> bool:
    header = file.file.read(4)
    file.file.seek(0)  
    return header == b'%PDF'

#  PNG signature
def is_png_file(file: UploadFile) -> bool:
    header = file.file.read(8)
    file.file.seek(0)  
    return header == b'\x89PNG\r\n\x1a\n'
@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    if file.filename.lower().endswith('.pdf'):
        if not is_pdf_file(file):
            raise HTTPException(status_code=400, detail="Invalid PDF file signature")
    if file.filename.lower().endswith('.png'):
        if not is_png_file(file):
            raise HTTPException(status_code=400, detail="Invalid PNG file signature")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    return {"filename": file.filename, "message": "File is valid"}

#jpeg signature
def is_jpeg_file(file: UploadFile) -> bool:
    header = file.file.read(3)
    file.file.seek(0)
    return header == b'\xFF\xD8\xFF'

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if file.filename.lower().endswith('.jpeg'):
        if not is_pdf_file(file):
            raise HTTPException(status_code=400, detail="Invalid PDF file signature")
    if file.filename.lower().endswith('.jpeg'):
        if not is_jpeg_file(file):
            raise HTTPException(status_code=400, detail="Invalid JPEG file signature")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    return {"filename": file.filename, "message": "File is valid"}


    
