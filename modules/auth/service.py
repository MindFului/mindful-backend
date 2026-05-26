import uuid, bcrypt, jwt
from datetime import datetime, timedelta
from core.config import SECRET_KEY, ALGORITHM
from core.database import supabase
from modules.organization.service import organizationService
from fastapi import HTTPException

class AuthService:
    def register(self, dto):
        """Registrar un nuevo usuario en Supabase"""
        email = dto.email.strip().lower()
        hashed = bcrypt.hashpw(dto.password.encode(), bcrypt.gensalt()).decode()
        organization = organizationService.get_organization_by_name(dto.organizationName)
        if not organization:
            raise HTTPException(status_code=400, detail="Organization not found")

        user_data = {
            "id": str(uuid.uuid4()),
            "email": email,
            "password": hashed,
            "role": dto.role,
            "nombre": dto.nombre,
            "apellido": dto.apellido,
            "telefono": dto.telefono,
            "documento_identidad": dto.documento_identidad,
            "grade": dto.grade,
            "section": dto.section,
            "organizationId": organization["id"]
        }
        
        try:
            result = supabase.table("users").insert(user_data).execute()

            error = getattr(result, "error", None)
            if error is not None:
                message = getattr(error, "message", str(error))
                raise HTTPException(status_code=400, detail=f"Supabase insert error: {message}")

            if not result.data:
                raise HTTPException(status_code=500, detail="Supabase insert returned no data")

            created = result.data[0]
            created.pop("password", None)
            return {"user": created}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error registering user: {e}")

    def login(self, dto):
        """Login y generación de JWT"""
        try:
            # Buscar usuario por email
            email = dto.email.strip().lower()
            result = supabase.table("users").select("*").eq("email", email).execute()
            
            if not result.data or len(result.data) == 0:
                raise HTTPException(status_code=401, detail="User not found")
            
            user = result.data[0]
            
            # Verificar password
            if not bcrypt.checkpw(dto.password.encode(), user["password"].encode()):
                raise HTTPException(status_code=401, detail="Invalid password")
            
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
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(status_code=500, detail=f"Error during login: {e}")

    def decode(self, token):
        """Decodificar JWT"""
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except:
            return None

auth_service = AuthService()