from db.connection import get_connection
from datetime import datetime
def createUser(username:str,email:str,hashed_password:str):
    conn=get_connection()
    cursor=conn.cursor()
    created_at=datetime.now().isoformat()
    cursor.execute("""
    insert into users(username,email,hashed_password,created_at) values(?,?,?,?)
""",(username,email,hashed_password,created_at,))
    row=cursor.lastrowid
    conn.commit()
    conn.close()
    return row

def get_userByEmail(email:str):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""select * from users where email=?""",(email,))
    row=cursor.fetchone()
    return row

def get_user_by_id(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row