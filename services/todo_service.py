from repositories.todo_repository import create_todo,update_todo,delete_todo,get_todos_by_user,delete_all_todos_repo,get_todos_count
from fastapi import HTTPException
import math
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
def get_all_todos_service(user_id: int, page: int = 1, limit: int = 5):
    rows = get_todos_by_user(user_id, page, limit)
    total = get_todos_count(user_id)
    total_pages = math.ceil(total / limit)
    
    return {
        "todos": [
            {
                "id": row[0],
                "title": row[1],
                "completed": bool(row[2]),
                "created_at": row[3]
            }
            for row in rows
        ],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages
        }
    }


def delete_all_todos_service(user_id:int):
    rows_affected=delete_all_todos_repo(user_id)
    return rows_affected
