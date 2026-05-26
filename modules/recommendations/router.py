# app/modules/recommendations/router.py
from fastapi import APIRouter
from modules.recommendations.service import rec_service

router = APIRouter()

@router.get("/{level}")
def rec(level: str):
    return {"recommendations": rec_service.recommend(level)}
