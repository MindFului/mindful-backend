# app/modules/users/router.py

from fastapi import APIRouter, HTTPException
from app.modules.users.service import users_service

router = APIRouter()

@router.get("/")
def get_all_users():
    return {"users": users_service.find_all()}

@router.get("/{id}")
def get_user(id: str):
    user = users_service.find_by_id(id)
    if not user:
        raise HTTPException(404, "User not found")
    return user

@router.patch("/{id}")
def update_user(id: str, body: dict):
    updated = users_service.update(id, body)
    if not updated:
        raise HTTPException(404, "User not found")
    return updated
