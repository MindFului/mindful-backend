# app/modules/admin/service.py
# Funciones administrativas básicas que consumen los servicios in-memory
from modules.users.service import users_service
from modules.tracking.service import tracking_service
from modules.workshops.service import workshops_service

class AdminService:
    def dashboard_summary(self):
        users = [u for u in users_service.find_all()] if hasattr(users_service, "find_all") else []
        workshops = workshops_service.list()
        recent_records = sorted(tracking_service.get_all_records(), key=lambda r: r["createdAt"], reverse=True) if hasattr(tracking_service, "get_all_records") else []
        return {
            "users_count": len(users),
            "workshops_count": len(workshops),
            "recent_records": recent_records[:10]
        }

admin_service = AdminService()
