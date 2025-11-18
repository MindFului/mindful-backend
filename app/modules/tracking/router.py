# app/modules/tracking/router.py
from fastapi import APIRouter, HTTPException
from app.modules.tracking.service import tracking_service
from app.modules.tracking.schemas import EmotionRecordDTO

router = APIRouter()

@router.post("/emotion")
def save(body: EmotionRecordDTO):
    return tracking_service.save_record(body)

@router.get("/user/{id}")
def get_user(id: str):
    return {"records": tracking_service.get_user_records(id)}
