from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.voice.router import router as voice_router
from app.modules.model.router import router as model_router
from app.modules.recommendations.router import router as rec_router
from app.modules.workshops.router import router as workshops_router
from app.modules.tracking.router import router as tracking_router

app = FastAPI(
    title="Mindful Backend API",
    description="Backend para plataforma Mindful con talleres y seguimiento emocional",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "message": "Mindful Backend API is running",
        "version": "1.0.0"
    }

# Routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(voice_router, prefix="/voice", tags=["Voice"])
app.include_router(model_router, prefix="/model", tags=["Model"])
app.include_router(rec_router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(workshops_router, prefix="/workshops", tags=["Workshops"])
app.include_router(tracking_router, prefix="/tracking", tags=["Tracking"])
