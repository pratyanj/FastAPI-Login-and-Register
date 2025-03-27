# auth_system/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form  # Add Form import
from fastapi.security import OAuth2PasswordRequestForm
from slowapi import Limiter
from slowapi.util import get_remote_address
from datetime import datetime

from core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from core.dependencies import get_current_user, oauth2_scheme

from config.settings import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

from models.schemas import UserResponse, TokenResponse  # Remove UserCreate import
from models.database import prisma
import re
router = APIRouter(tags=["Authentication"])
limiter = Limiter(key_func=get_remote_address)

# auth_system/routes/auth.py
@router.post(
    "/register",
    response_model=dict,
    description="Register a new user by submitting form data (not query parameters). Use the request body with Content-Type: application/x-www-form-urlencoded."
)
async def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    # Validate email format
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_pattern, email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    # Validate password strength
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    if not any(c.isupper() for c in password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter")
    if not any(c.isdigit() for c in password):
        raise HTTPException(status_code=400, detail="Password must contain at least one digit")

    # Validate password match
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords don't match")
    
    # Check for existing username or email
    existing_user = await prisma.user.find_first(
        where={
            "OR": [
                {"username": username},
                {"email": email}
            ]
        }
    )
    if existing_user:
        if existing_user.username == username:
            raise HTTPException(status_code=400, detail="Username already exists")
        if existing_user.email == email:
            raise HTTPException(status_code=400, detail="Email already exists")
    
    # Hash the password and create the user
    hashed_password = get_password_hash(password)
    new_user = await prisma.user.create(data={
        "username": username,
        "email": email,
        "password": hashed_password
    })
    return {"message": "User created successfully"}

@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await prisma.user.find_first(where={"username": form_data.username})
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    blacklisted = await prisma.blacklistedtoken.find_unique(where={"token": refresh_token})
    if blacklisted:
        raise HTTPException(status_code=401, detail="Refresh token has been invalidated")
    
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user


@router.post("/logout", response_model=dict)
async def logout(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        expires_at = datetime.utcfromtimestamp(payload.get("exp"))
        await prisma.blacklistedtoken.create({
            "data": {
                "token": token,
                "expiresAt": expires_at
            }
        })
        return {"message": "Successfully logged out"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")