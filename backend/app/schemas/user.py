from pydantic import BaseModel

# This schema defines exactly what data is sent back to the client when they request user information
class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    password_hash: str

    class Config:
        from_attributes = True
