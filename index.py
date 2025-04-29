from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

tasks = []

# Pydantic model for task
class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False

# Pydantic model for task update
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    task_dict = task.dict()
    task_dict["id"] = str(uuid.uuid4())
    tasks.append(task_dict)
    return task_dict

@app.get("/tasks/", response_model=List[Task])
async def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task_update: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            update_data = task_update.dict(exclude_unset=True)
            task.update(update_data)
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
