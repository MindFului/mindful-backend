from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
import jwt
from app.core.security import SECRET_KEY, ALGORITHM

auth_scheme = HTTPBearer()

async def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(401, "Missing token")
    token = token.split("Bearer ")[-1]
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        request.state.user = data
    except:
        raise HTTPException(401, "Invalid token")