import logging
import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core import client, db
from features import auth, marketplace, wallet, workspace
from seed_data import JOBS, TALENTS

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

app = FastAPI(title="Creator Resource Hub API (demo)")

for feature in (auth, marketplace, workspace, wallet):
    app.include_router(feature.router)


@app.get("/api/health")
async def health():
    return {"ok": True, "mode": "demo"}


@app.on_event("startup")
async def startup():
    await db.users.create_index("email", unique=True)
    await db.users.create_index("id", unique=True)
    await db.sessions.create_index("token_hash", unique=True)
    await db.shortlists.create_index([("user_id", 1), ("talent_id", 1)], unique=True)
    await db.unlocks.create_index([("user_id", 1), ("talent_id", 1)], unique=True)
    await db.applications.create_index([("user_id", 1), ("job_id", 1)], unique=True)
    for t in TALENTS:
        await db.talents.update_one({"id": t["id"]}, {"$set": t}, upsert=True)
    for j in JOBS:
        await db.jobs.update_one({"id": j["id"]}, {"$setOnInsert": j}, upsert=True)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ["CORS_ORIGINS"].split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
