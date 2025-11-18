import httpx
import os

class ModelService:
    def __init__(self):
        self.model_api_url = os.getenv("MODEL_API_URL", "http://localhost:5000")
        self.timeout = 30.0
    
    async def predict_audio(self, file):
        """
        Envía un archivo .wav al microservicio del modelo SVM
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                files = {"file": (file.filename, file.file, file.content_type)}
                response = await client.post(
                    f"{self.model_api_url}/predict_audio",
                    files=files
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPStatusError as e:
            return {"error": f"Modelo respondió error {e.response.status_code}", "details": str(e)}

        except httpx.RequestError as e:
            return {"error": "No se puede conectar con el microservicio del modelo", "details": str(e)}

        except Exception as e:
            return {"error": "Error inesperado", "details": str(e)}

model_service = ModelService()
