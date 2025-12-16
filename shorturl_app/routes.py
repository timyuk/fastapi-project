from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import HttpUrl

from db import add_url, get_url
from schemas import UrlCreate

router = APIRouter()

@router.post("/shorten", response_model=HttpUrl)
async def add_url_route(payload: UrlCreate, request: Request):
    url = await add_url(payload.url)
    return str(request.url_for("redirect_url", short_id=url['id']))



@router.get("/{short_id}", name="redirect_url")
async def get_url_route(short_id: int):
    url = await get_url(short_id)
    return RedirectResponse(
        url=url['url'],
        status_code=302
    )

@router.get("/stats/{short_id}")
async def get_stats_url_route(short_id: int):
    url = await get_url(short_id)
    return url

#
# @router.get("/items/{item_id}", response_model=TaskReturn)
# async def get_task_route(item_id: int):
#     task = await get_task(item_id)
#     if not task:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return task
#
# @router.put("/items/{item_id}")
# async def update_task_route(item_id: int, payload: TaskUpdate):
#     update_count = await update_task(item_id, payload.title, payload.description, payload.completed)
#     if not update_count:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return {"status": "ok"}
#
# @router.delete("/items/{item_id}")
# async def delete_task_route(item_id: int):
#     task = await delete_task(item_id)
#     if not task:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return {"status": "ok"}




