import random

class ModelService:
    def predict(self, features):
        score = random.random()
        if score < 0.4:
            level = "normal"
        elif score < 0.6:
            level = "mild"
        elif score < 0.8:
            level = "moderate"
        else:
            level = "high"
        return {"score": score, "level": level}

model_service = ModelService()