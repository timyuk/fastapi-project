from fastapi import APIRouter, HTTPException
from db import add_task, get_tasks, get_task, update_task, delete_task
from schemas import TaskCreate, TaskUpdate, TaskReturn

router = APIRouter()

@router.post("/items")
async def add_task_route(payload: TaskCreate):
    await add_task(payload.title, payload.description, payload.completed)
    return {"status": "ok"}

@router.get("/items", response_model=list[TaskReturn])
async def get_tasks_route():
    tasks = await get_tasks()
    return tasks

@router.get("/items/{item_id}", response_model=TaskReturn)
async def get_task_route(item_id: int):
    task = await get_task(item_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/items/{item_id}")
async def update_task_route(item_id: int, payload: TaskUpdate):
    update_count = await update_task(item_id, payload.title, payload.description, payload.completed)
    if not update_count:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "ok"}

@router.delete("/items/{item_id}")
async def delete_task_route(item_id: int):
    task = await delete_task(item_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "ok"}




