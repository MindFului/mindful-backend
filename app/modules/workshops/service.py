# app/modules/workshops/service.py
import uuid
from typing import List
from app.modules.workshops.schemas import WorkshopCreateDTO

workshops_db = []

class WorkshopsService:
    def list(self):
        return workshops_db

    def create(self, dto: WorkshopCreateDTO):
        workshop = {
            "id": str(uuid.uuid4()),
            "title": dto.title,
            "description": dto.description,
            "tags": dto.tags or [],
            "active": dto.active
        }
        workshops_db.append(workshop)
        return workshop

    def find_by_tags(self, tags: List[str]):
        return [
            w for w in workshops_db
            if w.get("active", True) and any(t in (w.get("tags") or []) for t in tags)
        ]

    def patch(self, wid: str, data: dict):
        for w in workshops_db:
            if w["id"] == wid:
                w.update(data)
                return w
        return None

    def delete(self, wid: str):
        global workshops_db
        workshops_db = [w for w in workshops_db if w["id"] != wid]
        return True

workshops_service = WorkshopsService()
