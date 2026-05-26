from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterDTO(BaseModel):
    email: EmailStr
    password: str
    role: str = "student"
    # Campos de perfil opcionales
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    documento_identidad: Optional[str] = None
    grade: Optional[str] = None
    section: Optional[str] = None
    organizationName: Optional[str] = None

class LoginDTO(BaseModel):
    email: EmailStr
    password: str
