# app/modules/workshops/service.py
import uuid
from typing import List
from app.modules.workshops.schemas import WorkshopCreateDTO, WorkshopUpdateDTO
from app.core.database import supabase

class WorkshopsService:
    def list(self):
        """Listar todos los workshops con información del propietario"""
        try:
            result = supabase.table("workshops") \
                .select("*, owner:users(id, email, nombre, apellido)") \
                .order("created_at", desc=True) \
                .execute()
            
            if result.data:
                # Aplanar la estructura del owner
                workshops = []
                for w in result.data:
                    workshop = dict(w)
                    if workshop.get("owner"):
                        owner = workshop.pop("owner")
                        workshop["owner_id"] = owner.get("id")
                        workshop["owner_email"] = owner.get("email")
                        workshop["owner_nombre"] = owner.get("nombre")
                        workshop["owner_apellido"] = owner.get("apellido")
                    workshops.append(workshop)
                return workshops
            return []
        except Exception as e:
            print(f"Error listing workshops: {e}")
            return []

    def find_by_id(self, wid: str):
        """Obtener un workshop por su ID con información del propietario"""
        try:
            result = supabase.table("workshops") \
                .select("*, owner:users(id, email, nombre, apellido)") \
                .eq("id", wid) \
                .single() \
                .execute()
            
            if result.data:
                workshop = dict(result.data)
                if workshop.get("owner"):
                    owner = workshop.pop("owner")
                    workshop["owner_id"] = owner.get("id")
                    workshop["owner_email"] = owner.get("email")
                    workshop["owner_nombre"] = owner.get("nombre")
                    workshop["owner_apellido"] = owner.get("apellido")
                return workshop
            return None
        except Exception as e:
            print(f"Error finding workshop by id: {e}")
            return None

    def create(self, dto: WorkshopCreateDTO, owner_id: str):
        """Crear un nuevo workshop"""
        # Convertir schedules a formato JSON
        schedules_json = [s.dict() if hasattr(s, 'dict') else s for s in (dto.schedules or [])]
        
        workshop_data = {
            "id": str(uuid.uuid4()),
            "title": dto.title,
            "description": dto.description,
            "image_url": dto.image_url,
            "tags": dto.tags or [],
            "active": dto.active,
            "ciudad": dto.ciudad,
            "direccion": dto.direccion,
            "referencia": dto.referencia,
            "schedules": schedules_json,
            "owner_id": owner_id
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
            result = supabase.table("workshops") \
                .select("*, owner:users(id, email, nombre, apellido)") \
                .eq("active", True) \
                .execute()
            
            # Filtrar por tags en Python
            if result.data:
                filtered = [
                    w for w in result.data
                    if w.get("tags") and any(t in w.get("tags", []) for t in tags)
                ]
                
                # Aplanar estructura del owner
                workshops = []
                for w in filtered:
                    workshop = dict(w)
                    if workshop.get("owner"):
                        owner = workshop.pop("owner")
                        workshop["owner_id"] = owner.get("id")
                        workshop["owner_email"] = owner.get("email")
                        workshop["owner_nombre"] = owner.get("nombre")
                        workshop["owner_apellido"] = owner.get("apellido")
                    workshops.append(workshop)
                return workshops
            return []
        except Exception as e:
            print(f"Error finding workshops by tags: {e}")
            return []

    def find_by_city(self, ciudad: str):
        """Buscar workshops por ciudad"""
        try:
            result = supabase.table("workshops") \
                .select("*, owner:users(id, email, nombre, apellido)") \
                .eq("ciudad", ciudad) \
                .eq("active", True) \
                .execute()
            
            if result.data:
                workshops = []
                for w in result.data:
                    workshop = dict(w)
                    if workshop.get("owner"):
                        owner = workshop.pop("owner")
                        workshop["owner_id"] = owner.get("id")
                        workshop["owner_email"] = owner.get("email")
                        workshop["owner_nombre"] = owner.get("nombre")
                        workshop["owner_apellido"] = owner.get("apellido")
                    workshops.append(workshop)
                return workshops
            return []
        except Exception as e:
            print(f"Error finding workshops by city: {e}")
            return []

    def patch(self, wid: str, data: dict):
        """Actualizar parcialmente un workshop"""
        try:
            # Remover campos que no se deben actualizar
            data.pop("id", None)
            data.pop("created_at", None)
            data.pop("owner_id", None)
            
            # Convertir schedules si existe
            if "schedules" in data and data["schedules"]:
                data["schedules"] = [
                    s.dict() if hasattr(s, 'dict') else s 
                    for s in data["schedules"]
                ]
            
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
