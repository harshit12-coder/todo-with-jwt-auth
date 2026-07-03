from pydantic import BaseModel
from typing import Any,Optional

class StandardResponse(BaseModel):
    success:bool
    message:str
    data:Optional[Any]=None

# Optional[Any] = None → 
# Data hoga toh do
# Nahi hoga toh None

def success_response(message: str, data: Any = None):
    return StandardResponse(
        success=True,
        message=message,
        data=data
    )

def error_response(message: str):
    return StandardResponse(
        success=False,
        message=message,
        data=None
    )