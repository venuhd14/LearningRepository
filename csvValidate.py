from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import hashlib
import os
import csv
from io import StringIO

app = FastAPI()

MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB 

UPLOAD_DIR = 'files'
os.makedirs(UPLOAD_DIR, exist_ok=True)
file_hashes = {}

def compute_file_hash(file):
    hash_algo = hashlib.sha256()
    while chunk := file.read(8192):
        hash_algo.update(chunk)
        file.seek(0)
        return hash_algo.hexdigest()
    
    
#upload csv file
@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    file_hash = compute_file_hash(file.file)
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")
    if file_hash in file_hashes:
        raise HTTPException(status_code=400, detail="File already uploaded")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, 'wb') as buffer:
        buffer.write(file.file.read())

    # Store the file hash
    file_hashes[file_hash] = file.filename

    return {"filename": file.filename, "hash": file_hash}

    
    # # Read the file
    # contents = await file.read()
    # if len(contents) > MAX_FILE_SIZE:
    #     raise HTTPException(status_code=400, detail="File is too large. Maximum size is 1MB.")
    # try:
    #     df = pd.read_csv(StringIO(contents.decode('utf-8')))
    # except pd.errors.EmptyDataError:
    #     raise HTTPException(status_code=400, detail="Uploaded file is empty or cannot be read.")
    # except pd.errors.ParserError:
    #     raise HTTPException(status_code=400, detail="Error parsing CSV file.")
    
    # #check for correct number of columns
    # expected_columns = ['Code', 'Symbol','Name']
       
    #     # expected_columns = ['Name', 'age','email']output will be false
    # if list(df.columns) != expected_columns:
    #     print("Header row does not match expected columns.")
    #     return False
    
    #  # check the datatype
    # if not pd.api.types.is_string_dtype(df['Code']):
    #     print("Name column should be of string type.")
    #     return False
    # if not pd.api.types.is_string_dtype(df['Symbol']):
    #     print("Symbol column should be of string type.")
    #     return False
    # if not pd.api.types.is_string_dtype(df['Name']):
    #     print("Name column should be of string type.")
    #     return False
   
    # #  convert into json format
    # try:
    #     json_data = df.to_dict(orient='records')
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Error converting data to JSON: {str(e)}")
    # return JSONResponse(content={"data": json_data})

    
# @app.post("/uploadproducts/")
# async def upload_file(file: UploadFile = File(...)):
#     if not file.filename.endswith('.csv'):
#         raise HTTPException(status_code=400, detail="Only CSV files are accepted.")
#     # return {"detail": "CSV file is valid."}

     
#      # Read the files
#     contents = await file.read()
#     try:
#         df = pd.read_csv(StringIO(contents.decode('utf-8')))
#     except pd.errors.EmptyDataError:
#         raise HTTPException(status_code=400, detail="Uploaded file is empty or cannot be read.")
#     except pd.errors.ParserError:
#         raise HTTPException(status_code=400, detail="Error parsing CSV file.")
    
#     #check for correct number of columns
#     expected_columns = ['Code', 'Symbol','Name']
#     if list(df.columns) != expected_columns:
#         print("Header row does not match expected columns.")
#         return False
    
#     # check the datatype
#     if not pd.api.types.is_string_dtype(df['Code']):
#         print("Name column should be of string type.")
#         return False
#     if not pd.api.types.is_string_dtype(df['Symbol']):
#         print("Symbol column should be of string type.")
#         return False
#     if not pd.api.types.is_string_dtype(df['Name']):
#         print("Name column should be of string type.")
#         return False
    
# #   convert into json format
#     try:
#         json_data = df.to_dict(orient='records')
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error converting data to JSON: {str(e)}")
#     return JSONResponse(content={"data": json_data})

