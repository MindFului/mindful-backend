# app/modules/tracking/schemas.py
from pydantic import BaseModel
from typing import Any

class EmotionRecordDTO(BaseModel):
    userId: str
    result: Any  # {level, score}
