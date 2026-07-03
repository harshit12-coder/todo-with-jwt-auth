from fastapi import APIRouter, Depends
from models.todo_model import CreateTodo, UpdateTodo
from models.response_model import success_response,error_response
from services.todo_service import (
    create_todo_service,
    update_todo_service, 
    delete_todo_service,
    get_all_todos_service
)
from core.security import verify_token

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.post("/")
def create_todo(request: CreateTodo, user=Depends(verify_token)):
    # user["user_id"] se user_id nikalo
    user_id=user["user_id"]
    # create_todo_service call karo
    success=create_todo_service(request.title,user_id)
    if success is None:
        return error_response("Todo couldn't be created")
    return success_response("Todo created✅",success)

@router.get("/")
def get_todos(user=Depends(verify_token)):
    # user["user_id"] se todos lo
    user_id=user["user_id"]
    rows=get_all_todos_service(user_id)
    return success_response("Your todos😀",rows)

@router.patch("/{todo_id}")
def update_todo(todo_id: int, request: UpdateTodo, user=Depends(verify_token)):
    rows_affected=update_todo_service(request.title,request.completed,todo_id)
    if rows_affected is None:
        return error_response("Something went wrong")
    return success_response("Todo Updated successfully",{"rows_affected":rows_affected})
    

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, user=Depends(verify_token)):
    user_id=user["user_id"]
    rows_affected=delete_todo_service(todo_id,user_id)
    if rows_affected is None:
         return error_response("Something went wrong")
    return success_response("Todo deleted successfully",{"rows_affected":rows_affected})
    
