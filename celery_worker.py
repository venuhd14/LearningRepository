import os
import time

from celery import Celery


celery = Celery('tasks',broker='redis://localhost:6379/0',backend='redis://localhost:6379/0')



@celery.task(name="create_task")
def create_task(task_type: int):
    print(f"task started with sleep time-- {task_type}")
    time.sleep(task_type)
    print(f"task finished after-- {task_type}")
    return True
