from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
import secrets
from app.core.config import settings

security = HTTPBasic()

users = {
    settings.BASIC_AUTH_USER: {
        "password": settings.BASIC_AUTH_PASSWORD,
        "role": "USER"
    },
    settings.BASIC_AUTH_ADMIN: {
        "password": settings.BASIC_AUTH_ADMIN_PASSWORD,
        "role": "ADMIN"
    }
}

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password

    if username not in users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user"
        )

    correct_password = users[username]["password"]

    if not secrets.compare_digest(password, correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

    return users[username]