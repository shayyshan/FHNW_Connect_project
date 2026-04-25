from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
import secrets

security = HTTPBasic()

# In-memory users (like Spring InMemoryUserDetailsManager)
users = {
    "myuser": {
        "password": "password",
        "role": "USER"
    },
    "myadmin": {
        "password": "password",
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