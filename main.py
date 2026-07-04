from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from db.connection import init_db
from routes.v1.auth_routes import router as v1_auth_router
from routes.v1.todo_routes import router as v1_todo_router
from core.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app = FastAPI(title="Jarvis API")

app.state.limiter=limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# bug fixing
# DB init
init_db()

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Something went wrong", "error": str(exc)}
    )

# 404 handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={"message": "Resource not found"}
    )

# Routes
app.include_router(v1_auth_router,prefix="/api/v1")
app.include_router(v1_todo_router,prefix="/api/v1")

@app.get("/")
def home():
    return {"message": "Jarvis API running 🚀"}