from fastapi import status, Depends, APIRouter, HTTPException
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

# create user
@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user : schemas.UserCreate, db : Session = Depends(get_db)):
    user_exist = db.query(models.UserModel).filter( models.UserModel.email == user.email).first()
    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with {user.email} already exist.")
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = models.UserModel(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    type(new_user)
    return new_user

# get user by id
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id : int, db : Session = Depends(get_db)):
    user_id = db.query(models.UserModel).filter(models.UserModel.id == id).first()

    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not found")
    
    return user_id
