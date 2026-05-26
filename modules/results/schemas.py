from pydantic import BaseModel
from typing import Optional

class ResultDTO(BaseModel):
    id: int
    user_id: str
    result: bool
    level: Optional[str] = None
    created_at: Optional[str] = None