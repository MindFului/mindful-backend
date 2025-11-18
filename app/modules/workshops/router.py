# app/modules/workshops/router.py
from fastapi import APIRouter, HTTPException
from app.modules.workshops.service import workshops_service
from app.modules.workshops.schemas import WorkshopCreateDTO

router = APIRouter()

@router.get("/")
def all_workshops():
    return {"workshops": workshops_service.list()}

@router.post("/")
def create_workshop(body: WorkshopCreateDTO):
    return workshops_service.create(body)

@router.patch("/{id}")
def patch_workshop(id: str, body: dict):
    w = workshops_service.patch(id, body)
    if not w:
        raise HTTPException(status_code=404, detail="Workshop not found")
    return w

@router.delete("/{id}")
def delete_workshop(id: str):
    workshops_service.delete(id)
    return {"ok": True}
