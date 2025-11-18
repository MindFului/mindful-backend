import uuid, bcrypt, jwt
from datetime import datetime, timedelta
from app.core.security import SECRET_KEY, ALGORITHM

users_db = []

class AuthService:
    def register(self, dto):
        hashed = bcrypt.hashpw(dto.password.encode(), bcrypt.gensalt()).decode()
        user = {
            "id": str(uuid.uuid4()),
            "email": dto.email,
            "password": hashed,
            "role": dto.role
        }
        users_db.append(user)
        return user

    def login(self, dto):
        user = next((u for u in users_db if u["email"] == dto.email), None)
        if not user:
            return None
        if not bcrypt.checkpw(dto.password.encode(), user["password"].encode()):
            return None
        payload = {
            "sub": user["id"],
            "email": user["email"],
            "role": user["role"],
            "exp": datetime.utcnow() + timedelta(days=7)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token

    def decode(self, token):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except:
            return None

auth_service = AuthService()