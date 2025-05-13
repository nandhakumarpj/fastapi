from fastapi import FastAPI


from app.routers import post, user
from app import models
from app.database import engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)