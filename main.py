from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List

app = FastAPI()


@app.post("/upload")
async def endpoint(uploaded_file: UploadFile):
    content = await uploaded_file.read()
    print(content)

# @app.post("/upload")
# async def endpoint(uploaded_file: bytes = File()):
#     content = uploaded_file
#     print(content)