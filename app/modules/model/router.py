from fastapi import APIRouter
from app.modules.model.service import model_service

router = APIRouter()

@router.post("/predict")
def predict(body: dict):
    return model_service.predict(body.get("features"))