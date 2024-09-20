from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from typing import List
from celery.result import AsyncResult
import asyncio
from fastapi.responses import JSONResponse
from celery_worker import create_task
# from pydantic import BaseModel
import logging

app = FastAPI()

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Single file upload
@app.post("/uploadfiles")
async def endpoint(uploaded_file: UploadFile):
    content = await uploaded_file.read()
    return {"filename": uploaded_file.filename, "content_type": uploaded_file.content_type}

    

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
    # logger.info(f"file {upload_file} requested")
    contents = await file.read()
    if file.content_type not in ("text/csv", "application/json"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV or JSON files are allowed.")    
    # logger.error(f"file {upload_file} requested")

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File is too large. Maximum size is 10 MB.")
    return {"filename": file.filename, "content_type": file.content_type}     
        
     

@app.post("/tasks")
def run_task(payload = Body(...)):
    print(payload)
    # task_type = payload.get("type")
    # print(task_type)
    # if task_type is None:
    #     raise ValueError("The 'type' key is missing or its value is None.")
    try:
        task = create_task.delay(int(0))
        print(task)
    except ValueError as e:
        raise ValueError(f"Invalid task type: {task_type}") from e
    return JSONResponse({"task_id": task.id})


@app.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id" : task_id, 
        "task_status" : task_result.state
        # "task_result" : task_result.result
        }
    return JSONResponse(result)
    


# @app.get("/")
# async def read_root():
#     logger.debug("Root endpoint accessed")
#     logger.info("Testing Info")
#     logger.warning("Testing Warning")
#     logger.error("Testing Error")
#     return {"message": "Hello World"}  

# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: str = None):
#     logger.info(f"Item {item_id} requested")
#     return {"item_id": item_id, "q": q}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)