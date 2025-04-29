from fastapi import FastAPI, HTTPException, Response, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models
from app.database import engine, get_db
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True        
    
@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    post_dict = post.model_dump()
    new_post = models.Post(**post_dict)
    db.add(new_post)
    db.commit()
    return {"data":new_post}

@app.get("/posts/{id}")
def get_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    return {"post_detail": post}
    
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False)
    db.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} doesnt exists")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    
    updated_post = db.query(models.Post).filter(models.Post.id == id).update({
       **post.model_dump()  
    }, synchronize_session=False)
    db.commit()
    if updated_post == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} doesnt exists")

    return {"data": updated_post}

