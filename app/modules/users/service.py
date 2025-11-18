# app/modules/users/service.py

from app.core.database import supabase

class UsersService:

    def find_by_id(self, user_id: str):
        """Buscar usuario por ID en Supabase"""
        try:
            result = supabase.table("users").select("*").eq("id", user_id).execute()
            if result.data and len(result.data) > 0:
                # No retornar el password en las consultas
                user = result.data[0]
                user.pop("password", None)
                return user
            return None
        except Exception as e:
            print(f"Error finding user by id: {e}")
            return None

    def find_all(self):
        """Obtener todos los usuarios"""
        try:
            result = supabase.table("users").select("id, email, role, created_at, updated_at").execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Error finding all users: {e}")
            return []

    def update(self, user_id: str, data: dict):
        """Actualizar datos del usuario"""
        try:
            # Remover campos que no se deben actualizar directamente
            data.pop("id", None)
            data.pop("created_at", None)
            
            result = supabase.table("users").update(data).eq("id", user_id).execute()
            if result.data and len(result.data) > 0:
                user = result.data[0]
                user.pop("password", None)
                return user
            return None
        except Exception as e:
            print(f"Error updating user: {e}")
            return None


users_service = UsersService()
