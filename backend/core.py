import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, Header, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv(Path(__file__).parent / ".env")

client = AsyncIOMotorClient(os.environ["MONGO_URL"])
db = client[os.environ["DB_NAME"]]
SESSION_TTL_HOURS = int(os.environ["SESSION_TTL_HOURS"])

TERMS_VERSION = "2026-01-demo"
GUIDELINES_VERSION = "2026-01-demo"
NO_ID = {"_id": 0}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def public_user(user: dict) -> dict:
    return {
        "id": user["id"],
        "email": user["email"],
        "display_name": user["display_name"],
        "capabilities": user["capabilities"],
        "mode": user["mode"],
        "consent": user.get("consent"),
        "token_balance": user["token_balance"],
        "is_demo": True,
    }


async def current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Not signed in")
    session = await db.sessions.find_one({"token_hash": hash_token(authorization[7:])}, NO_ID)
    if not session or session["expires_at"] < now_iso():
        raise HTTPException(401, "Session expired")
    user = await db.users.find_one({"id": session["user_id"]}, NO_ID)
    if not user:
        raise HTTPException(401, "Account not found")
    return user


async def consented_user(user: dict = Depends(current_user)) -> dict:
    if not user.get("consent"):
        raise HTTPException(403, "consent_required")
    return user


def require_capability(capability: str):
    async def checker(user: dict = Depends(consented_user)) -> dict:
        if capability not in user["capabilities"]:
            raise HTTPException(403, f"Your account cannot {capability}")
        return user

    return checker
