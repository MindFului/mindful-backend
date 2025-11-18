# app/modules/recommendations/service.py
class RecommendationsService:
    def recommend(self, level: str):
        rules = {
            "normal": ["grupo creativo"],
            "mild": ["mindfulness", "arte terapia"],
            "moderate": ["mindfulness guiado", "deporte grupal"],
            "high": ["derivación al psicólogo", "soporte estructurado"]
        }
        return rules.get(level, ["bienestar general"])

rec_service = RecommendationsService()
