from fastapi import FastAPI, Body, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session  
from celery.result import AsyncResult
from fastapi.responses import JSONResponse
from celery_worker.tasks import create_task  
import redis.asyncio as aioredis
import logging

app = FastAPI()

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    status = Column(String)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

redis_client = None

async def get_redis_client():
    global redis_client
    if redis_client is None:
        redis_client = await aioredis.from_url("redis://localhost:6379")
    return redis_client

@app.post("/tasks")
async def run_task(payload=Body(...), db: Session = Depends(get_db)):
    logger.info(f"Received payload: {payload}")
    try:
        task = create_task.delay(int(0))  # Start your Celery task
        logger.info(f"Task created with ID: {task.id}")

        # Save the task status to the database
        db_task = TaskModel(task_id=task.id, status=task.state)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)

    except ValueError as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    return JSONResponse({"task_id": task.id})

@app.get("/tasks/{task_id}")
async def get_status(task_id: str, db: Session = Depends(get_db)):
    task_result = AsyncResult(task_id)
    
    # Retrieve cached status from Redis if available
    client = await get_redis_client()
    cached_status = await client.get(task_id)

    # Fetch task status from the database
    db_task = db.query(TaskModel).filter(TaskModel.task_id == task_id).first()
    db_status = db_task.status if db_task else "No record found"

    result = {
        "task_id": task_id,
        "task_status": task_result.state,
        "cached_status": cached_status.decode("utf-8") if cached_status else "No cached status available",
        "db_status": db_status
    }
    return JSONResponse(result)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




