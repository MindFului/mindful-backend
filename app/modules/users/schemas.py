# app/modules/users/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    role: str = "student"

class StudentProfileDTO(BaseModel):
    nombre: str
    apellido: str
    telefono: str
    documento_identidad: str
    direccion: str

class OwnerWorkshopProfileDTO(BaseModel):
    nombre: str
    apellido: str
    telefono: str
    documento_identidad: str
    direccion: str

class UserCreateDTO(UserBase):
    password: str
    # Campos de perfil opcionales al crear
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    documento_identidad: Optional[str] = None
    direccion: Optional[str] = None

class UserUpdateDTO(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    documento_identidad: Optional[str] = None
    direccion: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    role: str
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    documento_identidad: Optional[str] = None
    direccion: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
