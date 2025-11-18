# app/modules/tracking/service.py
import uuid
from datetime import datetime
from typing import List
from app.modules.tracking.schemas import EmotionRecordDTO
from app.core.database import supabase

class TrackingService:
    def save_record(self, dto: EmotionRecordDTO):
        """Guardar registro de emoción en Supabase"""
        record_data = {
            "id": str(uuid.uuid4()),
            "user_id": dto.userId,
            "result": dto.result  # Se guarda como JSONB
        }
        
        try:
            result = supabase.table("emotion_records").insert(record_data).execute()
            if result.data and len(result.data) > 0:
                return result.data[0]
            return None
        except Exception as e:
            print(f"Error saving emotion record: {e}")
            return None

    def get_user_records(self, user_id: str):
        """Obtener todos los registros de un usuario"""
        try:
            result = supabase.table("emotion_records") \
                .select("*") \
                .eq("user_id", user_id) \
                .order("created_at", desc=True) \
                .execute()
            
            return result.data if result.data else []
        except Exception as e:
            print(f"Error getting user records: {e}")
            return []

tracking_service = TrackingService()
