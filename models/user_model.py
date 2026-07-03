from pydantic import BaseModel,EmailStr,field_validator

class UserSignUp(BaseModel):
    username:str
    email:EmailStr
    password:str

    @field_validator("password")
    def validate_password(cls,value):
# field_validator mein:
# cls → hamesha likhna hai (Pydantic chahiye)
# value → tera actual data
        if len(value)<8:
            raise ValueError("Password kam se kam 8 characters ka hona chaiye")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password mein kam se kam ek number hona chahiye")
        if not any(char.isalpha() for char in value):
            raise ValueError("Password mein kam se kam ek letter hona chahiye")
        if not any(char in "!@#$%^&*" for char in value):
            raise ValueError("Password mein kam se kam ek special character hona chahiye (!@#$%^&*)")
        return value


class UserLogin(BaseModel):
    email:EmailStr
    password:str

class RefreshTokenRequest(BaseModel):
    refresh_token: str