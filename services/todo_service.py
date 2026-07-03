from repositories.todo_repository import create_todo,update_todo,delete_todo,get_todos_by_user
from fastapi import HTTPException
def create_todo_service(title:str,user_id:int):
    if title.strip() == "":
        raise HTTPException(status_code=400,detail="title cannot be empty")
    if user_id is None:
        raise HTTPException(status_code=400,detail="User_id can not be empty")
    row_id=create_todo(title,user_id)
    return row_id

def update_todo_service(title:str,completed:bool,id:int):
    rows_affected=update_todo(title,completed,id)
    return rows_affected

def delete_todo_service(id:int,user_id:int):
    rows_affected=delete_todo(id,user_id)
    return rows_affected
def get_all_todos_service(user_id:int):
    rows=get_todos_by_user(user_id)
    return [
        {
            "id":row[0],
            "title":row[1],
            "completed":row[2],
            "created_at":row[3]
        }
        for row in rows
    ]



