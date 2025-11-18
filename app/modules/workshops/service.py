# app/modules/workshops/service.py
import uuid
from typing import List
from app.modules.workshops.schemas import WorkshopCreateDTO
from app.core.database import supabase

class WorkshopsService:
    def list(self):
        """Listar todos los workshops"""
        try:
            result = supabase.table("workshops").select("*").order("created_at", desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Error listing workshops: {e}")
            return []

    def create(self, dto: WorkshopCreateDTO):
        """Crear un nuevo workshop"""
        workshop_data = {
            "id": str(uuid.uuid4()),
            "title": dto.title,
            "description": dto.description,
            "tags": dto.tags or [],
            "active": dto.active
        }
        
        try:
            result = supabase.table("workshops").insert(workshop_data).execute()
            if result.data and len(result.data) > 0:
                return result.data[0]
            return None
        except Exception as e:
            print(f"Error creating workshop: {e}")
            return None

    def find_by_tags(self, tags: List[str]):
        """Buscar workshops por tags (activos)"""
        try:
            # Supabase usa operador @> para arrays (contains)
            result = supabase.table("workshops").select("*").eq("active", True).execute()
            
            # Filtrar por tags en Python (alternativa: usar RPC con función SQL personalizada)
            if result.data:
                filtered = [
                    w for w in result.data
                    if w.get("tags") and any(t in w.get("tags", []) for t in tags)
                ]
                return filtered
            return []
        except Exception as e:
            print(f"Error finding workshops by tags: {e}")
            return []

    def patch(self, wid: str, data: dict):
        """Actualizar parcialmente un workshop"""
        try:
            # Remover campos que no se deben actualizar
            data.pop("id", None)
            data.pop("created_at", None)
            
            result = supabase.table("workshops").update(data).eq("id", wid).execute()
            if result.data and len(result.data) > 0:
                return result.data[0]
            return None
        except Exception as e:
            print(f"Error patching workshop: {e}")
            return None

    def delete(self, wid: str):
        """Eliminar un workshop"""
        try:
            supabase.table("workshops").delete().eq("id", wid).execute()
            return True
        except Exception as e:
            print(f"Error deleting workshop: {e}")
            return False

workshops_service = WorkshopsService()
