from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from taskService.db.database import get_db
import taskService.db.models
import taskService.db.schemas
import redis
import json
import os
from datetime import datetime
import httpx

router = APIRouter()
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", "6379"))
CACHE_EXPIRE_SECONDS = int(os.getenv("CACHE_EXPIRE_SECONDS", 1800))  # 30 минут
auth_url = os.getenv("AUTH_URL", "http://auth-service:8001")

redis_conn = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@router.get("/tasks", response_model=List[schemas.Task])
async def list_tasks(token:str, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{auth_url}/user", headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
           raise HTTPException(status_code=401, detail="Invalid token")
        user = response.json()
    cached_tasks = redis_conn.get(f"tasks:{user['id']}")
    if cached_tasks:
       return json.loads(cached_tasks)
    user_tasks = db.query(models.Task).filter(models.Task.owner_id == user["id"]).all()
    redis_conn.setex(f"tasks:{user['id']}", CACHE_EXPIRE_SECONDS, json.dumps([schemas.Task(**task.__dict__) for task in user_tasks]))
    return user_tasks

@router.post("/tasks", response_model=schemas.Task)
async def create_task(task:schemas.TaskCreate, token:str, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{auth_url}/user", headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
             raise HTTPException(status_code=401, detail="Invalid token")
        user = response.json()
    new_task = models.Task(owner_id = user["id"], **task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    cached_tasks = redis_conn.get(f"tasks:{user['id']}")
    if cached_tasks:
        user_tasks = json.loads(cached_tasks)
        user_tasks.append(schemas.Task(**new_task.__dict__))
        redis_conn.setex(f"tasks:{user['id']}", CACHE_EXPIRE_SECONDS, json.dumps(user_tasks))
    return new_task

@router.put("/tasks/{id}", response_model=schemas.Task)
async def update_task(id: str, task:schemas.TaskUpdate, token:str, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{auth_url}/user", headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = response.json()
    db_task = db.query(models.Task).filter(models.Task.id == id, models.Task.owner_id == user["id"]).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = task.title
    db_task.completed = task.completed
    db.commit()
    db.refresh(db_task)
    redis_conn.delete(f"tasks:{user['id']}")
    return db_task

@router.delete("/tasks/{id}")
async def delete_task(id: str, token:str, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{auth_url}/user", headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = response.json()
    db_task = db.query(models.Task).filter(models.Task.id == id, models.Task.owner_id == user["id"]).first()
    if not db_task:
       raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    redis_conn.delete(f"tasks:{user['id']}")
    return {"message": "Task deleted"}
