# app/modules/users/router.py

from fastapi import APIRouter, HTTPException
from modules.users.service import users_service

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
@router.get("/organization/{organization_id}")
def get_users_by_organization(organization_id: str):
    users = users_service.get_by_organization(organization_id)
    return {"users": users}

@router.patch("/{id}")
def update_user(id: str, body: dict):
    updated = users_service.update(id, body)
    if not updated:
        raise HTTPException(404, "User not found")
    return updated
