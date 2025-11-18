from fastapi import FastAPI
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.voice.router import router as voice_router
from app.modules.model.router import router as model_router
from app.modules.recommendations.router import router as rec_router
from app.modules.workshops.router import router as workshops_router
from app.modules.tracking.router import router as tracking_router

app = FastAPI(title="Mindful Backend - FastAPI")

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(voice_router, prefix="/voice", tags=["Voice"])
app.include_router(model_router, prefix="/model", tags=["Model"])
app.include_router(rec_router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(workshops_router, prefix="/workshops", tags=["Workshops"])
app.include_router(tracking_router, prefix="/tracking", tags=["Tracking"])