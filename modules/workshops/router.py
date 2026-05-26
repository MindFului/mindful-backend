# app/modules/workshops/router.py
from fastapi import APIRouter, HTTPException, Query
from modules.workshops.service import workshops_service
from modules.workshops.schemas import WorkshopCreateDTO, WorkshopUpdateDTO, WorkshopStatus
from typing import List, Optional

router = APIRouter()

@router.get("/")
def all_workshops(status: Optional[WorkshopStatus] = Query(None, description="Filtrar por status: active, inactive, pending")):
    # Convertir el enum a string si existe
    status_str = status.value if status else None
    return {"workshops": workshops_service.list(status=status_str)}

@router.get("/{id}")
def get_workshop_by_id(id: str):
    workshop = workshops_service.find_by_id(id)
    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")
    return workshop

@router.get("/by-city/{ciudad}")
def workshops_by_city(ciudad: str):
    return {"workshops": workshops_service.find_by_city(ciudad)}

@router.get("/by-tags")
def workshops_by_tags(tags: List[str]):
    return {"workshops": workshops_service.find_by_tags(tags)}

@router.post("/")
def create_workshop(body: WorkshopCreateDTO):
    workshop = workshops_service.create(body, owner_id=None)
    if not workshop:
        raise HTTPException(status_code=500, detail="Error creating workshop")
    return workshop

@router.patch("/{id}")
def patch_workshop(id: str, body: WorkshopUpdateDTO):
    data = body.dict(exclude_unset=True)
    w = workshops_service.patch(id, data)
    if not w:
        raise HTTPException(status_code=404, detail="Workshop not found")
    return w

@router.delete("/{id}")
def delete_workshop(id: str):
    success = workshops_service.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Workshop not found")
    return {"ok": True}
