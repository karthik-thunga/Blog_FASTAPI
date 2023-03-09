from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional, Any
from pydantic.types import conint

class PostBase(BaseModel):
    title : str
    content : str
    is_published : bool

class PostCreate(PostBase):
    tags : Optional[list[str]] = []

    class Config:
        arbitrary_types_allowed = True

class UserOut(BaseModel):
    first_name : Optional[str]
    last_name : Optional[str]
    email : EmailStr
    is_active : Optional[bool]

    class Config:
        orm_mode = True
class Comment_create(BaseModel):
    comment : str
    post_id : int

class Comment_out(Comment_create):
    user_id : int

    class Config:
        orm_mode = True

class TagOut(BaseModel):
    name : str

    class Config:
        orm_mode = True

class PostOut(PostBase):
    id : int
    created_at : datetime
    last_updated : datetime
    owner_id : int
    owner : UserOut
    post_comment : list[Comment_out]
    votes : Optional[int] = 0
    tags : Optional[list[TagOut]] = []
    
    @validator('tags')
    def extract_tag_names(cls, v):
        return [tag.name for tag in v] if v else []  # extract tag names from tags list

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    first_name : Optional[str]
    last_name : Optional[str]
    email : EmailStr
    password : str
    is_active : Optional[bool]

class UserOut(BaseModel):
    first_name : Optional[str]
    last_name : Optional[str]
    email : EmailStr
    is_active : Optional[bool]

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str]

class Vote(BaseModel):
    post_id : int
    dir : conint(le=1)

