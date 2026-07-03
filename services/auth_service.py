from repositories.user_repository import createUser,get_userByEmail,get_user_by_id
from repositories.refresh_token_repository import save_refresh_token,get_refresh_token,revoke_refresh_token
from fastapi import HTTPException
from passlib.context import CryptContext
from core.security import create_token,create_refresh_token
from core.logger import logger
from datetime import datetime,timedelta,timezone
def signUpService(username:str,email:str,password:str):
    logger.info(f"SignUp:{username,email}")
    if username.strip()== "":
        
        raise HTTPException(status_code=400,detail="Bad request! username cannot be Empty")
    if email.strip() == "":
        raise HTTPException(status_code=400,detail="Bad request! email cannot be Empty")
    if password.strip() =="":
        raise HTTPException(status_code=400,detail="Bad request! password cannot be Empty")
    isEmailAlreadyExist=get_userByEmail(email)
    
    if isEmailAlreadyExist:
        logger.warning(f"Email {email} already exists")
        return {"message": "Email already exists"} 
    # Hashiing kro
    pwd_context=CryptContext(schemes=["bcrypt"])
    hashed_password=pwd_context.hash(password)
    row=createUser(username,email,hashed_password)
    logger.info(f"Signup successful: {email}")
    return row


def loginService(email:str,password:str):
     logger.info(f"Login Attempt: {email}")
     if email.strip() == "":
        raise HTTPException(status_code=400,detail="Bad request! email cannot be Empty")
     if password.strip() =="":
        raise HTTPException(status_code=400,detail="Bad request! password cannot be Empty")
     row=get_userByEmail(email)
     if row is None:
        logger.warning(f"Login failed — user not found: {email}")
        raise HTTPException(status_code=404, detail="User not found")
     
     hashed_password=row[3]
     pwd_context=CryptContext(schemes=["bcrypt"])
     success=pwd_context.verify(password,hashed_password)
     if not success:
         logger.warning(f"Login failed — wrong password: {email}")
         raise HTTPException(status_code=401,detail="Unaithorized or invalid creds entered")
     logger.info(f"Login Success for {email}")
     user_id=row[0]
     email=row[2]
     token=create_token(user_id,email)
     refresh_token=create_refresh_token(user_id,email)
     expires_at=datetime.now(timezone.utc)+timedelta(minutes=15)
     expires_at = expires_at.isoformat()
     save_refresh_token(user_id,refresh_token,expires_at)
     return {"Access token":token,"Refresh Token":refresh_token,"token_type":"Bearer"}

def refreshTokenService(refresh_token: str):
    # 1. DB mein dhundho
    row = get_refresh_token(refresh_token)
    
    # 2. Exist karta hai?
    if row is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    # 3. Revoked check karo
    # row[4] = is_revoked
    if row[4] == 1:
        raise HTTPException(status_code=401, detail="Token revoked")
    
    # 4. Expiry check karo
    # row[3] = expires_at (string)
    expires_at = datetime.fromisoformat(row[3])
    if datetime.now(timezone.utc) > expires_at:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    
    # 5. Naya access token banao
    user_id = row[1]  # row[1] = user_id
    
    # user ki email chahiye — DB se lo
    user = get_user_by_id(user_id)  # ← Yeh banana padega
    
    new_token = create_token(user_id, user[2])  # user[2] = email
    return {"access_token": new_token, "token_type": "Bearer"}