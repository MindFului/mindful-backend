# run.py - Script para desarrollo local
# Para producción, usa directamente: uvicorn app.main:app o gunicorn

import uvicorn

if __name__ == "__main__":
    print("🚀 Iniciando servidor de desarrollo...")
    print("📖 Documentación: http://localhost:8000/docs")
    print("🔍 Health check: http://localhost:8000/")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Hot reload para desarrollo
        log_level="info"
    )
