# app/modules/tracking/service.py
import uuid
from datetime import datetime
from typing import List
from app.modules.tracking.schemas import EmotionRecordDTO

tracking_db = []

class TrackingService:
    def save_record(self, dto: EmotionRecordDTO):
        record = {
            "id": str(uuid.uuid4()),
            "userId": dto.userId,
            "result": dto.result,
            "createdAt": datetime.utcnow().isoformat()
        }
        tracking_db.append(record)
        return record

    def get_user_records(self, user_id: str):
        return [r for r in tracking_db if r["userId"] == user_id]

tracking_service = TrackingService()
