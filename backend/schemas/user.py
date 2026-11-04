from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=255)


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    is_active: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=255)
class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut