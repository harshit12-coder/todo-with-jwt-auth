from db.connection import get_connection
from datetime import datetime

def create_todo(title:str,user_id:int):
    conn=get_connection()
    cursor=conn.cursor()
    created_at=datetime.now().isoformat()
    cursor.execute("""
insert into todos(title, completed, created_at, user_id) 
values(?, 0, ?, ?)
""",(title,created_at,user_id,))
    row=cursor.lastrowid
    conn.commit()
    conn.close()
    return row

def update_todo(title: str, completed: bool, id: int):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Sirf jo values hain unhe update karo
    if title is not None and completed is not None:
        cursor.execute("""
            UPDATE todos SET completed=?, title=? WHERE id=?
        """, (int(completed), title, id))
    elif title is not None:
        cursor.execute("""
            UPDATE todos SET title=? WHERE id=?
        """, (title, id))
    elif completed is not None:
        cursor.execute("""
            UPDATE todos SET completed=? WHERE id=?
        """, (int(completed), id))
    
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected

def get_todos_by_user(user_id: int, page: int = 1, limit: int = 5):
    conn = get_connection()
    cursor = conn.cursor()
    offset = (page - 1) * limit
    cursor.execute("""
        SELECT * FROM todos 
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """, (user_id, limit, offset))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_todos_count(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM todos 
        WHERE user_id = ?
    """, (user_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def delete_todo(id:int,user_id:int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        delete FROM todos 
        WHERE id = ? and user_id=?
    """, (id,user_id))
    rows_affected=cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected

def delete_all_todos_repo(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        delete FROM todos 
        WHERE user_id=?
    """, (user_id,))
    rows_affected=cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected