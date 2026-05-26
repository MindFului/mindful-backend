from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from modules.auth.schemas import RegisterDTO, LoginDTO
from modules.auth.service import auth_service

router = APIRouter()

# Security scheme para Swagger (activa el botón "Authorize")
security = HTTPBearer()

@router.post("/register")
def register(dto: RegisterDTO):
    return auth_service.register(dto)

@router.post("/login")
def login(dto: LoginDTO):
    token = auth_service.login(dto)
    return {"token": token}

@router.get("/me")
def me(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    credentials.scheme -> 'Bearer'
    credentials.credentials -> '<token>'
    """
    token = credentials.credentials
    data = auth_service.decode(token)

    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return data
