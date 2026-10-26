import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Literal, Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, EmailStr, Field

from core import (GUIDELINES_VERSION, NO_ID, SESSION_TTL_HOURS, TERMS_VERSION, current_user, db,
                  hash_token, now_iso, public_user)
from seed_data import WELCOME_GRANT, user_workspace_seed

router = APIRouter(prefix="/api/auth", tags=["auth"])


class DemoSessionIn(BaseModel):
    intent: Literal["signin", "signup"]
    email: EmailStr
    display_name: Optional[str] = Field(None, max_length=60)


class ConsentIn(BaseModel):
    accept_terms: bool
    accept_guidelines: bool
    terms_version: str


class ModeIn(BaseModel):
    mode: Literal["hiring", "working"]


async def _create_user(email: str, name: str) -> dict:
    uid = str(uuid.uuid4())
    user = {"id": uid, "email": email, "display_name": name, "capabilities": ["hire", "work"],
            "mode": "hiring", "consent": None, "token_balance": WELCOME_GRANT, "created_at": now_iso()}
    await db.users.insert_one(dict(user))
    seed = user_workspace_seed(uid)
    await db.threads.insert_many(seed["threads"])
    await db.messages.insert_many(seed["messages"])
    await db.tasks.insert_many(seed["tasks"])
    await db.privacy_settings.insert_one(seed["settings"])
    await db.ledger.insert_one({"id": str(uuid.uuid4()), "user_id": uid, "amount": WELCOME_GRANT,
                                "kind": "grant", "label": "Welcome grant (demo)", "created_at": now_iso()})
    return user


@router.post("/demo-session")
async def demo_session(body: DemoSessionIn):
    email = body.email.lower()
    user = await db.users.find_one({"email": email}, NO_ID)
    if body.intent == "signin" and not user:
        raise HTTPException(404, "No demo account for this email yet. Use Sign up instead.")
    if body.intent == "signup":
        if user:
            raise HTTPException(409, "A demo account already exists for this email. Use Sign in.")
        user = await _create_user(email, (body.display_name or email.split("@")[0]).strip())
    token = secrets.token_urlsafe(32)
    expires = (datetime.now(timezone.utc) + timedelta(hours=SESSION_TTL_HOURS)).isoformat()
    await db.sessions.insert_one({"token_hash": hash_token(token), "user_id": user["id"],
                                  "created_at": now_iso(), "expires_at": expires})
    return {"token": token, "user": public_user(user)}


@router.get("/me")
async def me(user: dict = Depends(current_user)):
    return public_user(user)


@router.post("/consent")
async def consent(body: ConsentIn, user: dict = Depends(current_user)):
    if not (body.accept_terms and body.accept_guidelines):
        raise HTTPException(400, "Both the Terms and Community Guidelines must be accepted")
    if body.terms_version != TERMS_VERSION:
        raise HTTPException(400, "Outdated terms version, please reload")
    record = {"terms_version": TERMS_VERSION, "guidelines_version": GUIDELINES_VERSION, "accepted_at": now_iso()}
    await db.users.update_one({"id": user["id"]}, {"$set": {"consent": record}})
    return public_user({**user, "consent": record})


@router.put("/me/mode")
async def set_mode(body: ModeIn, user: dict = Depends(current_user)):
    needed = "hire" if body.mode == "hiring" else "work"
    if needed not in user["capabilities"]:
        raise HTTPException(403, "This account cannot use that mode")
    await db.users.update_one({"id": user["id"]}, {"$set": {"mode": body.mode}})
    return public_user({**user, "mode": body.mode})


@router.post("/sign-out")
async def sign_out(authorization: Optional[str] = Header(None)):
    if authorization and authorization.startswith("Bearer "):
        await db.sessions.delete_one({"token_hash": hash_token(authorization[7:])})
    return {"ok": True}


@router.get("/legal")
async def legal():
    return {"terms_version": TERMS_VERSION, "guidelines_version": GUIDELINES_VERSION}
