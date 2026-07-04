from fastapi import APIRouter,Request
from models.user_model import UserSignUp, UserLogin,RefreshTokenRequest
from services.auth_service import signUpService, loginService,refreshTokenService
from models.response_model import success_response,error_response
from core.limiter import limiter
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
@limiter.limit("3/hour")
def signup(request:Request,body: UserSignUp):
    result = signUpService( body.username, body.email, body.password)
    return success_response("User created ✅", result)

@router.post("/login")
@limiter.limit("5/minute")
def login(request:Request,body: UserLogin):
    result = loginService(body.email, body.password)
    return success_response("Login Successful ✅", result)

@router.post("/refresh")
def refresh_token(request:RefreshTokenRequest):
    data=refreshTokenService(request.refresh_token)
    return success_response("Token refreshed ✅", data)