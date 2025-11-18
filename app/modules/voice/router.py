from fastapi import APIRouter, File, UploadFile
from app.modules.voice.service import voice_service

router = APIRouter()

@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    features = await voice_service.extract_features(content)
    return {"features": features}