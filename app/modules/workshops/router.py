# app/modules/workshops/router.py
from fastapi import APIRouter, HTTPException, Depends, Header
from app.modules.workshops.service import workshops_service
from app.modules.workshops.schemas import WorkshopCreateDTO, WorkshopUpdateDTO
from app.modules.auth.service import auth_service
from typing import Optional, List

router = APIRouter()

def get_current_user_id(authorization: Optional[str] = Header(None)):
    """Extraer user_id del token JWT (si existe)"""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    token = authorization.replace("Bearer ", "")
    payload = auth_service.decode(token)
    if payload:
        return payload.get("sub")
    return None

@router.get("/")
def all_workshops():
    return {"workshops": workshops_service.list()}

@router.get("/by-city/{ciudad}")
def workshops_by_city(ciudad: str):
    return {"workshops": workshops_service.find_by_city(ciudad)}

@router.get("/by-tags")
def workshops_by_tags(tags: List[str]):
    return {"workshops": workshops_service.find_by_tags(tags)}

@router.post("/")
def create_workshop(body: WorkshopCreateDTO, user_id: str = Depends(get_current_user_id)):
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    workshop = workshops_service.create(body, owner_id=user_id)
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
