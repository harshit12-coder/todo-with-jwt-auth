import sqlite3
from dotenv import load_dotenv
import os
load_dotenv()
DB_NAME=os.getenv("DB_NAME","todoProdDB.db")
def get_connection():
    conn=sqlite3.connect(DB_NAME)
    return conn

def init_db():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""
    create table if not exists users(
                   id integer primary key autoincrement,
                   username text not null,
                   email text not null unique,
                   hashed_password text not null,
                   created_at text not null
                   )

    """)
    cursor.execute("""create table if not exists todos(
                   id integer primary key autoincrement,
                   title text not null,
                   completed integer default 0,
                   created_at text not null,
                   user_id integer not null,
                   foreign key (user_id) references users(id)
                   )""")
    cursor.execute("""create table if not exists refresh_tokens(
                   id integer primary key autoincrement,
                   user_id integer not null,
                   token text not null,
                   expires_at text not null,
                   is_revoked integer default 0,
                   foreign key (user_id) references users(id)
                   
                   )""")
    conn.commit()
    conn.close()
    print("DB is ready ✌️")
