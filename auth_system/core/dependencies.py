# auth_system/core/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config.settings import SECRET_KEY, ALGORITHM
from models.database import prisma

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str ):
    blacklisted = await prisma.blacklistedtoken.find_unique(where={"token": token})
    if blacklisted:
        raise HTTPException(status_code=401, detail="Token has been invalidated")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = await prisma.user.find_first(where={"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user