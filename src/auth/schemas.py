from pydantic import BaseModel, EmailStr


class TokenPayload(BaseModel):
    token: str

class TokenPairSchema(BaseModel):
    access: str
    refresh: str


class AccessTokenSchema(BaseModel):
    access: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


