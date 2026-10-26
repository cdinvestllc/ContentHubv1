import re
import uuid
from typing import List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from core import NO_ID, consented_user, db, now_iso, require_capability
from seed_data import CATEGORIES

router = APIRouter(prefix="/api", tags=["marketplace"])
PUBLIC_TALENT = {"_id": 0, "contact": 0}


class JobIn(BaseModel):
    title: str = Field(min_length=6, max_length=100)
    category: str
    budget_min: int = Field(ge=10, le=100000)
    budget_max: int = Field(ge=10, le=100000)
    budget_type: Literal["fixed", "day", "per item"]
    deadline: str
    description: str = Field(min_length=20, max_length=2000)
    deliverables: List[str] = Field(default_factory=list, max_length=10)
    skills: List[str] = Field(default_factory=list, max_length=10)


class ApplyIn(BaseModel):
    cover_note: str = Field(min_length=20, max_length=1500)
    rate: int = Field(ge=10, le=100000)


def _search(q: Optional[str], fields: List[str]) -> dict:
    if not q:
        return {}
    rx = {"$regex": re.escape(q.strip()), "$options": "i"}
    return {"$or": [{f: rx} for f in fields]}


async def _talent_flags(user_id: str, talents: List[dict]) -> List[dict]:
    ids = [t["id"] for t in talents]
    shortlisted = {d["talent_id"] async for d in db.shortlists.find({"user_id": user_id, "talent_id": {"$in": ids}})}
    unlocked = {d["talent_id"] async for d in db.unlocks.find({"user_id": user_id, "talent_id": {"$in": ids}})}
    return [{**t, "is_shortlisted": t["id"] in shortlisted, "contact_unlocked": t["id"] in unlocked} for t in talents]


@router.get("/categories")
async def categories():
    return CATEGORIES


@router.get("/talent")
async def list_talent(q: Optional[str] = None, category: Optional[str] = None, user: dict = Depends(consented_user)):
    query = _search(q, ["name", "headline", "skills", "location"])
    if category:
        query["category"] = category
    talents = await db.talents.find(query, PUBLIC_TALENT).to_list(100)
    return await _talent_flags(user["id"], talents)


@router.get("/talent/{talent_id}")
async def get_talent(talent_id: str, user: dict = Depends(consented_user)):
    talent = await db.talents.find_one({"id": talent_id}, NO_ID)
    if not talent:
        raise HTTPException(404, "Talent not found")
    contact = talent.pop("contact")
    [result] = await _talent_flags(user["id"], [talent])
    result["contact"] = contact if result["contact_unlocked"] else None
    return result


@router.get("/shortlist")
async def get_shortlist(user: dict = Depends(consented_user)):
    ids = [d["talent_id"] async for d in db.shortlists.find({"user_id": user["id"]}).sort("created_at", -1)]
    talents = await db.talents.find({"id": {"$in": ids}}, PUBLIC_TALENT).to_list(100)
    return await _talent_flags(user["id"], talents)


@router.put("/shortlist/{talent_id}")
async def add_shortlist(talent_id: str, user: dict = Depends(consented_user)):
    if not await db.talents.find_one({"id": talent_id}):
        raise HTTPException(404, "Talent not found")
    await db.shortlists.update_one({"user_id": user["id"], "talent_id": talent_id},
                                   {"$setOnInsert": {"created_at": now_iso()}}, upsert=True)
    return {"ok": True}


@router.delete("/shortlist/{talent_id}")
async def remove_shortlist(talent_id: str, user: dict = Depends(consented_user)):
    await db.shortlists.delete_one({"user_id": user["id"], "talent_id": talent_id})
    return {"ok": True}


def _job_view(job: dict, user_id: str, applied: set) -> dict:
    out = {k: v for k, v in job.items() if k != "owner_id"}
    out["is_owner"] = job["owner_id"] == user_id
    out["has_applied"] = job["id"] in applied
    return out


@router.get("/jobs")
async def list_jobs(q: Optional[str] = None, category: Optional[str] = None,
                    scope: Literal["open", "mine"] = "open", user: dict = Depends(consented_user)):
    query = _search(q, ["title", "brand", "skills", "description"])
    if category:
        query["category"] = category
    query["owner_id"] = user["id"] if scope == "mine" else {"$ne": user["id"]}
    jobs = await db.jobs.find(query, NO_ID).sort([("boosted", -1), ("posted_at", -1)]).to_list(100)
    applied = {d["job_id"] async for d in db.applications.find({"user_id": user["id"]})}
    return [_job_view(j, user["id"], applied) for j in jobs]


@router.get("/jobs/{job_id}")
async def get_job(job_id: str, user: dict = Depends(consented_user)):
    job = await db.jobs.find_one({"id": job_id}, NO_ID)
    if not job:
        raise HTTPException(404, "Job not found")
    applied = {d["job_id"] async for d in db.applications.find({"user_id": user["id"], "job_id": job_id})}
    return _job_view(job, user["id"], applied)


@router.post("/jobs", status_code=201)
async def create_job(body: JobIn, user: dict = Depends(require_capability("hire"))):
    if body.budget_max < body.budget_min:
        raise HTTPException(400, "Maximum budget must be at least the minimum")
    if body.category not in {c["slug"] for c in CATEGORIES}:
        raise HTTPException(400, "Unknown category")
    job = {**body.model_dump(), "id": f"job-{uuid.uuid4().hex[:10]}", "brand": user["display_name"],
           "owner_id": user["id"], "location": "Remote", "urgency": "standard", "boosted": False,
           "posted_at": now_iso(), "applicants_count": 0, "is_demo": True}
    await db.jobs.insert_one(dict(job))
    return _job_view(job, user["id"], set())


@router.post("/jobs/{job_id}/apply", status_code=201)
async def apply_job(job_id: str, body: ApplyIn, user: dict = Depends(require_capability("work"))):
    job = await db.jobs.find_one({"id": job_id}, NO_ID)
    if not job:
        raise HTTPException(404, "Job not found")
    if job["owner_id"] == user["id"]:
        raise HTTPException(400, "You cannot apply to your own job")
    if await db.applications.find_one({"user_id": user["id"], "job_id": job_id}):
        raise HTTPException(409, "You already applied to this job")
    await db.applications.insert_one({"id": str(uuid.uuid4()), "job_id": job_id, "user_id": user["id"],
                                      "cover_note": body.cover_note, "rate": body.rate, "created_at": now_iso()})
    await db.jobs.update_one({"id": job_id}, {"$inc": {"applicants_count": 1}})
    return {"ok": True, "simulated": True}
