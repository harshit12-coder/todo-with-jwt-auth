# from core.security import create_refresh_token
from db.connection import get_connection

def save_refresh_token(user_id:int,token:str,expires_at:str):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(""" insert into refresh_tokens(user_id,token,expires_at,is_revoked) values(?,?,?,0)""",(user_id,token,expires_at,)
            )
    row=cursor.lastrowid
    conn.commit()
    conn.close()
    return row

def get_refresh_token(token:str):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""select * from refresh_tokens where token=?""",(token,))
    row=cursor.fetchone()
    conn.commit()
    conn.close()
    return row

def revoke_refresh_token(token:str):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""update refresh_tokens set is_revoked=1 where token=?""",(token,))
    rows_affected=cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected