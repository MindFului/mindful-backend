# app/modules/workshops/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class UbicacionDTO(BaseModel):
    ciudad: str
    direccion: str
    referencia: Optional[str] = None

class ScheduleDTO(BaseModel):
    dia: str  # e.g., "Lunes", "Martes"
    hora_inicio: str  # e.g., "09:00"
    hora_fin: str  # e.g., "17:00"

class WorkshopCreateDTO(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[List[str]] = []
    active: Optional[bool] = True
    # Ubicación
    ciudad: str
    direccion: str
    referencia: Optional[str] = None
    # Horarios
    schedules: Optional[List[ScheduleDTO]] = []
    # Usuario propietario (se asignará automáticamente desde el token JWT)
    # owner_id se agregará en el service

class WorkshopUpdateDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[List[str]] = None
    active: Optional[bool] = None
    ciudad: Optional[str] = None
    direccion: Optional[str] = None
    referencia: Optional[str] = None
    schedules: Optional[List[ScheduleDTO]] = None

class WorkshopResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    image_url: Optional[str]
    tags: Optional[List[str]]
    active: bool
    ciudad: str
    direccion: str
    referencia: Optional[str]
    schedules: Optional[List[dict]]
    owner_id: Optional[str] = None
    # Información del propietario (joined)
    owner_email: Optional[str] = None
    owner_nombre: Optional[str] = None
    owner_apellido: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
