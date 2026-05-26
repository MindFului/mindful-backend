from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.auth.router import router as auth_router
from modules.users.router import router as users_router
from modules.model.router import router as model_router
from modules.recommendations.router import router as rec_router
from modules.workshops.router import router as workshops_router
from modules.tracking.router import router as tracking_router
from modules.results.router import router as results_router
from modules.organization.router import router as organization_router
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
app.include_router(organization_router, prefix="/organizations", tags=["Organizations"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(results_router, prefix="/results", tags=["Results"])
app.include_router(model_router, prefix="/model", tags=["Model"])
app.include_router(rec_router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(workshops_router, prefix="/workshops", tags=["Workshops"])
app.include_router(tracking_router, prefix="/tracking", tags=["Tracking"])
