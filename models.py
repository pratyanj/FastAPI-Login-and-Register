from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str

class User(BaseModel):
    username: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_new_password: str
    
class BlacklistedToken (BaseModel):
    id : int
    token : str
    expiresAt : datetime