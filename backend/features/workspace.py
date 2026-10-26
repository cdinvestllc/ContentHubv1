import uuid
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from core import consented_user, db, now_iso

router = APIRouter(prefix="/api", tags=["workspace"])


class MessageIn(BaseModel):
    body: str = Field(min_length=1, max_length=2000)


class TaskStatusIn(BaseModel):
    status: Literal["todo", "in_progress", "review", "done"]


class PrivacyIn(BaseModel):
    public_profile: bool
    show_rates: bool
    allow_direct_messages: bool
    incognito_browsing: bool
    show_in_search: bool


@router.get("/inbox")
async def list_threads(user: dict = Depends(consented_user)):
    return await db.threads.find({"user_id": user["id"]}, {"_id": 0}).sort("updated_at", -1).to_list(100)


async def _own_thread(thread_id: str, user_id: str) -> dict:
    thread = await db.threads.find_one({"id": thread_id, "user_id": user_id}, {"_id": 0})
    if not thread:
        raise HTTPException(404, "Conversation not found")
    return thread


@router.get("/inbox/{thread_id}")
async def get_thread(thread_id: str, user: dict = Depends(consented_user)):
    thread = await _own_thread(thread_id, user["id"])
    messages = await db.messages.find({"thread_id": thread_id, "user_id": user["id"]}, {"_id": 0}).sort("created_at", 1).to_list(500)
    await db.threads.update_one({"id": thread_id}, {"$set": {"unread": 0}})
    return {**thread, "unread": 0, "messages": messages}


@router.post("/inbox/{thread_id}/messages", status_code=201)
async def send_message(thread_id: str, body: MessageIn, user: dict = Depends(consented_user)):
    await _own_thread(thread_id, user["id"])
    msg = {"id": str(uuid.uuid4()), "thread_id": thread_id, "user_id": user["id"], "sender": "me",
           "body": body.body.strip(), "created_at": now_iso(), "simulated": True}
    await db.messages.insert_one(dict(msg))
    await db.threads.update_one({"id": thread_id}, {"$set": {"updated_at": msg["created_at"]}})
    return msg


@router.get("/tasks")
async def list_tasks(user: dict = Depends(consented_user)):
    return await db.tasks.find({"user_id": user["id"]}, {"_id": 0}).sort("due", 1).to_list(500)


@router.patch("/tasks/{task_id}")
async def move_task(task_id: str, body: TaskStatusIn, user: dict = Depends(consented_user)):
    res = await db.tasks.find_one_and_update({"id": task_id, "user_id": user["id"]},
                                             {"$set": {"status": body.status}}, projection={"_id": 0}, return_document=True)
    if not res:
        raise HTTPException(404, "Task not found")
    return res


@router.get("/settings/privacy")
async def get_privacy(user: dict = Depends(consented_user)):
    doc = await db.privacy_settings.find_one({"user_id": user["id"]}, {"_id": 0, "user_id": 0})
    if not doc:
        raise HTTPException(404, "Settings not found")
    return doc


@router.put("/settings/privacy")
async def update_privacy(body: PrivacyIn, user: dict = Depends(consented_user)):
    await db.privacy_settings.update_one({"user_id": user["id"]}, {"$set": body.model_dump()}, upsert=True)
    return body.model_dump()
