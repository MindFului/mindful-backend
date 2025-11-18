class VoiceService:
    async def extract_features(self, file_bytes):
        return {"mfcc": [0.1, 0.2, 0.3], "energy": 0.87}

voice_service = VoiceService()