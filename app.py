from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base
import crud
from contextlib import asynccontextmanager

import schemas

Base.metadata.create_all(bind=engine)
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    db: Session = next(get_db())
    crud.seed_initial_data(db)  
    yield

# Create the FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/api/posts")
def get_posts(
    status: str = None, 
    include: str = None, 
    db: Session = Depends(get_db)
):
    include_list = include.split(",") if include else []
    posts = crud.get_posts(db=db, status=status, include=include_list)

    if not posts:
        raise HTTPException(status_code=404, detail="Posts not found")
    return posts

@app.get("/api/posts/{post_id}")
def get_post(
    post_id: str, 
    include: str = None, 
    db: Session = Depends(get_db)
):
    include_list = include.split(",") if include else []
    post = crud.get_post_by_id(db=db, post_id=post_id, include=include_list)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.get("/api/users/{user_id}")
def get_user(
    user_id: str, 
    include: str = None, 
    db: Session = Depends(get_db)
):
    include_list = include.split(",") if include else []
    user = crud.get_user_by_id(db=db, user_id=user_id, include=include_list)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
