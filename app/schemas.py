from pydantic import BaseModel, EmailStr
from datetime import datetime
    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class Post(BaseModel):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        
class UserBase(BaseModel):
    email: EmailStr
    password: str
    class Config:
        from_attributes = True
        
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True
        
class UserCreate(UserBase):
    pass