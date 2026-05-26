# app/modules/admin/router.py
from fastapi import APIRouter
from modules.admin.service import admin_service

router = APIRouter()

@router.get("/summary")
def summary():
    return admin_service.dashboard_summary()
