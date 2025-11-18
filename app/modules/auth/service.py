import uuid, bcrypt, jwt
from datetime import datetime, timedelta
from app.core.config import SECRET_KEY, ALGORITHM
from app.core.database import supabase

class AuthService:
    def register(self, dto):
        """Registrar un nuevo usuario en Supabase"""
        hashed = bcrypt.hashpw(dto.password.encode(), bcrypt.gensalt()).decode()
        user_data = {
            "id": str(uuid.uuid4()),
            "email": dto.email,
            "password": hashed,
            "role": dto.role
        }
        
        try:
            result = supabase.table("users").insert(user_data).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            print(f"Error registering user: {e}")
            return None

    def login(self, dto):
        """Login y generación de JWT"""
        try:
            # Buscar usuario por email
            result = supabase.table("users").select("*").eq("email", dto.email).execute()
            
            if not result.data or len(result.data) == 0:
                return None
            
            user = result.data[0]
            
            # Verificar password
            if not bcrypt.checkpw(dto.password.encode(), user["password"].encode()):
                return None
            
            # Generar JWT
            payload = {
                "sub": user["id"],
                "email": user["email"],
                "role": user["role"],
                "exp": datetime.utcnow() + timedelta(days=7)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
            return token
        except Exception as e:
            print(f"Error during login: {e}")
            return None

    def decode(self, token):
        """Decodificar JWT"""
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except:
            return None

auth_service = AuthService()