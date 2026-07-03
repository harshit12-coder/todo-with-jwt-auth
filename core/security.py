from jose import jwt,JWTError
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta,timezone
from dotenv import load_dotenv
import os
load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

oauth2_sceheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

# jwt.encode  → algorithm  → String  "HS256"
# jwt.decode  → algorithms → List   ["HS256"]

def create_token(user_id:int,email:str):
    payload={
        "user_id":user_id,
        "email":email,
        "type":"access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10)
    }
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

# refresh token
def create_refresh_token(user_id:int,email:str):
    payload={
         "user_id":user_id,
        "email":email,
        "type":"refresh",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
    }
    refresh_token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return refresh_token


def verify_token(token:str=Depends(oauth2_sceheme)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email=payload.get("email")
        user_id=payload.get("user_id")
        if email is None:
            raise HTTPException(status_code=401,detail="Invalid request/token")
        if user_id is None:
             raise HTTPException(status_code=401,detail="Invalid request/token")
        return {"user_id":user_id,"email":email}
    except JWTError:
       raise HTTPException(status_code=401,detail="Invalid request/token")

