# app/modules/workshops/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class WorkshopCreateDTO(BaseModel):
    title: str
    description: Optional[str] = None
    tags: Optional[List[str]] = []
    active: Optional[bool] = True

class WorkshopResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    tags: Optional[List[str]]
    active: bool
