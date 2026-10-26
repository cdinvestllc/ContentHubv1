import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from pymongo import ReturnDocument

from core import NO_ID, consented_user, db, now_iso
from seed_data import BOOST_COST, BUNDLES, UNLOCK_COST

router = APIRouter(prefix="/api/wallet", tags=["wallet"])


class UnlockIn(BaseModel):
    talent_id: str


class BoostIn(BaseModel):
    job_id: str


class TopupIn(BaseModel):
    bundle_id: str


async def _debit(user_id: str, cost: int, label: str) -> int:
    updated = await db.users.find_one_and_update(
        {"id": user_id, "token_balance": {"$gte": cost}}, {"$inc": {"token_balance": -cost}},
        projection=NO_ID, return_document=ReturnDocument.AFTER)
    if not updated:
        raise HTTPException(402, f"Not enough Tokens. This action costs {cost}.")
    await db.ledger.insert_one({"id": str(uuid.uuid4()), "user_id": user_id, "amount": -cost, "kind": "spend",
                                "label": label, "created_at": now_iso()})
    return updated["token_balance"]


@router.get("")
async def wallet(user: dict = Depends(consented_user)):
    ledger = await db.ledger.find({"user_id": user["id"]}, {"_id": 0, "user_id": 0}).sort("created_at", -1).to_list(200)
    return {"balance": user["token_balance"], "ledger": ledger, "bundles": BUNDLES,
            "prices": {"unlock_contact": UNLOCK_COST, "boost_job": BOOST_COST}}


@router.post("/unlock-contact")
async def unlock_contact(body: UnlockIn, user: dict = Depends(consented_user)):
    talent = await db.talents.find_one({"id": body.talent_id}, NO_ID)
    if not talent:
        raise HTTPException(404, "Talent not found")
    if await db.unlocks.find_one({"user_id": user["id"], "talent_id": body.talent_id}):
        return {"balance": user["token_balance"], "contact": talent["contact"], "charged": 0}
    balance = await _debit(user["id"], UNLOCK_COST, f"Unlocked contact · {talent['name']}")
    await db.unlocks.insert_one({"user_id": user["id"], "talent_id": body.talent_id, "created_at": now_iso()})
    return {"balance": balance, "contact": talent["contact"], "charged": UNLOCK_COST}


@router.post("/boost-job")
async def boost_job(body: BoostIn, user: dict = Depends(consented_user)):
    job = await db.jobs.find_one({"id": body.job_id, "owner_id": user["id"]}, NO_ID)
    if not job:
        raise HTTPException(404, "You can only boost your own jobs")
    if job.get("boosted"):
        raise HTTPException(409, "This job is already boosted")
    balance = await _debit(user["id"], BOOST_COST, f"Boosted job · {job['title']}")
    await db.jobs.update_one({"id": body.job_id}, {"$set": {"boosted": True}})
    return {"balance": balance, "charged": BOOST_COST}


@router.post("/demo-topup")
async def demo_topup(body: TopupIn, user: dict = Depends(consented_user)):
    bundle = next((b for b in BUNDLES if b["id"] == body.bundle_id), None)
    if not bundle:
        raise HTTPException(400, "Unknown bundle")
    updated = await db.users.find_one_and_update({"id": user["id"]}, {"$inc": {"token_balance": bundle["tokens"]}},
                                                 projection=NO_ID, return_document=ReturnDocument.AFTER)
    await db.ledger.insert_one({"id": str(uuid.uuid4()), "user_id": user["id"], "amount": bundle["tokens"],
                                "kind": "topup", "label": f"{bundle['label']} (simulated, no payment)",
                                "created_at": now_iso()})
    return {"balance": updated["token_balance"], "simulated": True}
