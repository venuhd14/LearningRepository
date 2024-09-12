
# # from fastapi import FastAPI, File, UploadFile, HTTPException
# # from fastapi.middleware.cors import CORSMiddleware
# # from typing import List
# # from .validators import validate_csv
# # import csv
# # import pandas as pd
# # from io import StringIO

# # app = FastAPI()

# # #cors
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=["*"],
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )


# # @app.post("/upload/")
# # async def upload_file(file: UploadFile = File(...)):
# #     if not file.filename.endswith(".csv"):
# #         raise HTTPException(status_code=400, detail= "invalid datatype")
# #     contents = await file.read()
# #     try:
# #         df.pd.read_csv(StringIO(contents.decode("utf-8")))
# #     except pd.errors.EmptyDataError:
# #         raise HTTPException(status_code=400, detail = "uplaoded file is empty and cannot be read")
# #     except pd.errors.ParserError:
# #         raise HTTPException(status_code=400,detail="Error Parsing CSV file")
    
 
# # @app.   



# from fastapi import FastAPI, File, UploadFile, HTTPException
# from pydantic import BaseModel
# import hashlib
# from typing import List
# import os

# app = FastAPI()

# # Directory to store uploaded files
# UPLOAD_DIR = 'files'
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # Dictionary to store file hashes (for simplicity)
# file_hashes = {}

# def compute_file_hash(file):
#     hash_algo = hashlib.sha256()
#     while chunk := file.read(8192):
#         hash_algo.update(chunk)
#     file.seek(0)  # Reset file pointer to the beginning
#     return hash_algo.hexdigest()

# @app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     file_hash = compute_file_hash(file.file)
#     if not file.filename.endswith(".csv"):
#         raise HTTPException(status_code=400, detail="only csv file are accepted.")
#     if file_hash in file_hashes:
#         raise HTTPException(status_code=400, detail="File already uploaded")

#     # Save file
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, 'wb') as buffer:
#         buffer.write(file.file.read())

#     # Store the file hash
#     file_hashes[file_hash] = file.filename

#     return {"filename": file.filename, "hash": file_hash}

# @app.get("/")
# def read_root():
#     return {"message": "Upload your files at /upload/"}


    
# # from fastapi import FastAPI, File, UploadFile, HTTPException
# # import hashlib
# # import os
# # from typing import List

# # app = FastAPI()

# # # Directory to store uploaded files
# # UPLOAD_DIR = 'uploads'
# # os.makedirs(UPLOAD_DIR, exist_ok=True)

# # # Dictionary to store file hashes (for simplicity)
# # file_hashes = {}

# # def compute_file_hash(file):
# #     hash_algo = hashlib.sha256()
# #     chunk = file.read(8192)
# #     while chunk:
# #         hash_algo.update(chunk)
# #         chunk = file.read(8192)
# #     file.seek(0)  # Reset file pointer to the beginning
# #     return hash_algo.hexdigest()

# # @app.post("/upload/")
# # async def upload_files(files: List[UploadFile] = File(...)):
# #     response = {"files": []}

# #     for file in files:
# #         file_hash = compute_file_hash(file.file)

# #         if file_hash in file_hashes:
# #             response["files"].append({"filename": file.filename, "status": "already uploaded"})
# #             continue
        
# #         file_path = os.path.join(UPLOAD_DIR, file.filename)
# #         with open(file_path, 'wb') as buffer:
# #             buffer.write(file.file.read())

# #         file_hashes[file_hash] = file.filename
# #         response["files"].append({"filename": file.filename, "status": "uploaded"})

# #     return response

# # @app.post("/upload_single/")
# # async def upload_single_file(file: UploadFile = File(...)):
# #     file_hash = compute_file_hash(file.file)

# #     if file_hash in file_hashes:
# #         raise HTTPException(status_code=400, detail="File already uploaded")

# #     file_path = os.path.join(UPLOAD_DIR, file.filename)
# #     with open(file_path, 'wb') as buffer:
# #         buffer.write(file.file.read())

# #     file_hashes[file_hash] = file.filename

# #     return {"filename": file.filename, "status": "uploaded"}

# # @app.get("/")
# # def read_root():
# #     return {"message": "Upload your files at /upload/ for multiple files or /upload_single/ for a single file"}

