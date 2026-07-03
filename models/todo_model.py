from pydantic import BaseModel
from typing import Optional

class CreateTodo(BaseModel):
    title:str

class UpdateTodo(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None