from fastapi import APIRouter, Depends, HTTPException
from typing import List
import redis
import json
import os
from datetime import datetime
import httpx
import schemas #Изменили импорт
router = APIRouter()
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", "6379"))
CACHE_EXPIRE_SECONDS = int(os.getenv("CACHE_EXPIRE_SECONDS", 1800))  # 30 минут
auth_url = os.getenv("AUTH_URL", "http://localhost:8001")
db_url = os.getenv("DB_URL", "http://localhost:8003")
redis_conn = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@router.get("/tasks", response_model=List[schemas.Task])
async def list_tasks(token:str):
   async with httpx.AsyncClient() as client:
        response = await client.get(f"{auth_url}/user", headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
          raise HTTPException(status_code=401, detail="Invalid token")
        user = response.json()
   cached_tasks = redis_conn.get(f"tasks:{user['id']}")
   if cached_tasks:
      return json.loads(cached_tasks)
   async with httpx.AsyncClient() as client:
       response = await client.get(f"{db_url}/tasks/{user['id']}")
       if response.status_code != 200:
           raise HTTPException(status_code=response.status_code, detail=response.json().get("detail"))
       user_tasks = response.json()
       redis_conn.setex(f"tasks:{user['id']}", CACHE_EXPIRE_SECONDS, json.dumps([schemas.Task(**task) for task in user_tasks]))
       return user_tasks

@router.post("/tasks", response_model=schemas.Task)
async def create_task(task:schemas.TaskCreate, token:str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{auth_url}/user", headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
           raise HTTPException(status_code=401, detail="Invalid token")
        user = response.json()
        response = await client.post(f"{db_url}/tasks", json=task.model_dump(), params={"user_id": user["id"]})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail"))
        new_task = response.json()
    cached_tasks = redis_conn.get(f"tasks:{user['id']}")
    if cached_tasks:
       user_tasks = json.loads(cached_tasks)
       user_tasks.append(schemas.Task(**new_task))
       redis_conn.setex(f"tasks:{user['id']}", CACHE_EXPIRE_SECONDS, json.dumps(user_tasks))
    return new_task

@router.put("/tasks/{id}", response_model=schemas.Task)
async def update_task(id: str, task:schemas.TaskUpdate, token:str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{auth_url}/user", headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = response.json()
        response = await client.put(f"{db_url}/tasks/{id}", json=task.model_dump())
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail"))
        db_task = response.json()
    redis_conn.delete(f"tasks:{user['id']}")
    return db_task

@router.delete("/tasks/{id}")
async def delete_task(id: str, token:str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{auth_url}/user", headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
           raise HTTPException(status_code=401, detail="Invalid token")
        user = response.json()
        response = await client.delete(f"{db_url}/tasks/{id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail"))
    redis_conn.delete(f"tasks:{user['id']}")
    return {"message": "Task deleted"}
