from pydantic import BaseModel

class User(BaseModel):
    user_id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class UserSummary(BaseModel):
    user_id: int
    username: str

    class Config:
        from_attributes = True

# Legacy support
class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    password_hash: str

    class Config:
        from_attributes = True
