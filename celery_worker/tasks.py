import os
import time
import json
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@celery.task(name="create_task")
def create_task(task_type: int):
    print(f"Task started with sleep time: {task_type} seconds")
    time.sleep(task_type)
    print(f"Task finished after: {task_type} seconds")
    
    result = {
        "success": True,
        "message": f"Task completed after {task_type} seconds",
        "task_type": task_type
    }
    
    return json.dumps(result) 

