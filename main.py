from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List

app = FastAPI()


@app.post("/upload")
async def endpoint(uploaded_file: UploadFile):
    print(uploaded_file.file)
    print(uploaded_file._in_memory)
    content = await uploaded_file.read()
    print(content)

# @app.post("/upload")
# async def endpoint(uploaded_file: bytes = File()):
#     content = uploaded_file
#     print(content)