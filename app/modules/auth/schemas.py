from pydantic import BaseModel

class RegisterDTO(BaseModel):
    email: str
    password: str
    role: str = "student"

class LoginDTO(BaseModel):
    email: str
    password: str