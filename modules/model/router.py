from fastapi import APIRouter, UploadFile, File
from modules.model.service import model_service

router = APIRouter()

@router.post("/predict_audio")
async def predict_audio(file: UploadFile = File(...),score: int = 0,idUser: str = ""):
    """
    Envía audio .wav al microservicio del modelo SVM
    """
    result = await model_service.predict_audio(file,score,idUser)
    return result
