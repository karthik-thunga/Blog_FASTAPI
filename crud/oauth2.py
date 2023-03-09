from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta
from . import schemas
from .database import get_db
from sqlalchemy.orm import Session
from .models import UserModel
from .config import settings

oauth2_scheme = OAuth2PasswordBearer('login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})

    token = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return token

def verify_access_token(token : str, credential_exception):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        id : str = payload.get("user_id")
        if not id:
            raise credential_exception
        token_data = schemas.TokenData(id=id)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sesssion expired")
    except JWTError:
        raise credential_exception

    return token_data


def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                        detail="Could not validate credentials", 
                                        headers={"WWW-Authenticate" : "Bearer"})

    token_data = verify_access_token(token=token, credential_exception= credential_exception)
    user = db.query(UserModel).filter(UserModel.id == token_data.id).first()

    return user