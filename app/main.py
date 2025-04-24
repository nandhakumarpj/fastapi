from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from dotenv import load_dotenv
import os

load_dotenv()

db_host = os.getenv('db_host')
db_name = os.getenv('db_name')
db_user = os.getenv('db_user')
db_password = os.getenv('db_password')


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:  
    try:
        conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print('Database connection failed')
        print('Error: ', error)
        time.sleep(2)
        
    
@app.get("/posts")
async def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts")
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data":new_post}

@app.get("/posts/{id}")
def get_posts(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    return {"post_detail": post}
    
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} doesnt exists")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} doesnt exists")
    post_dict = updated_post
    return {"data": post_dict}
