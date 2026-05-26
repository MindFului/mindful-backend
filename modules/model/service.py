import httpx
import os
from modules.results.service import resultsService
class ModelService:
    def __init__(self):
        self.model_api_url = os.getenv("MODEL_API_URL")
        self.timeout = 30.0
    
    async def predict_audio(self, file, score,idUser):
        """
        Envía un archivo .wav al microservicio del modelo SVM
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                files = {"file": (file.filename, file.file, file.content_type)}
                response = await client.post(
                    f"{self.model_api_url}/predict_audio",
                    files=files,
                    data={"score": str(score)}
                )
                response.raise_for_status()

                payload = response.json()
                prediction = payload.get("prediction", {})
                descripcion = (prediction.get("descripcion") or "").strip().lower()
                result_value = 1 if descripcion == "con depresión" else 0

                fusion = payload.get("fusion", {})
                level = fusion.get("risk_level")
                print(f"Predicción: {descripcion}, Nivel de riesgo: {level}")
                # Guardar resultado en la base de datos
                resultsService.process_save(
                    idUser,
                    {"result": result_value},
                    level
                )

                return payload

        except httpx.HTTPStatusError as e:
            return {"error": f"Modelo respondió error {e.response.status_code}", "details": str(e)}

        except httpx.RequestError as e:
            return {"error": "No se puede conectar con el microservicio del modelo", "details": str(e)}

        except Exception as e:
            return {"error": "Error inesperado", "details": str(e)}

model_service = ModelService()
