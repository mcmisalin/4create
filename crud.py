from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from models import Post, User, Comment, Tag
import schemas

def seed_initial_data(db: Session):
    # Check if users exist to avoid duplicate inserts
    if db.query(User).count() == 0:
        # Insert users
        db.add_all([
            User(username='john_doe'),
            User(username='jane_smith')
        ])

    # Check if tags exist to avoid duplicate inserts
    if db.query(Tag).count() == 0:
        # Insert tags
        db.add_all([
            Tag(name='python'),
            Tag(name='fastapi')
        ])

    # Check if posts exist to avoid duplicate inserts
    if db.query(Post).count() == 0:
        # Insert posts without tags initially
        user1 = db.query(User).filter(User.username == 'john_doe').first()
        user2 = db.query(User).filter(User.username == 'jane_smith').first()

        python_tag = db.query(Tag).filter_by(name="python").first()
        fastapi_tag = db.query(Tag).filter_by(name="fastapi").first()
        
        post1 = Post(post_text='First post about Python', draft=False, user_id=user1.id)
        post2 = Post(post_text='Exploring FastAPI', draft=True, user_id=user2.id)
        
        tag_python = db.query(Tag).filter(Tag.name == 'python').first()
        tag_fastapi = db.query(Tag).filter(Tag.name == 'fastapi').first()
        
        post1.tags.append(tag_python) 
        post2.tags.append(tag_fastapi)  
        post2.tags.append(tag_python)  
        
        db.add_all([post1, post2])
        db.commit()

        db.commit()


def get_posts(db: Session, status: str = None, include: list = []):
    query = db.query(Post)
    
    if status:
        if status == "1":
            query = query.filter(Post.draft == True)
        elif status == "0":
            query = query.filter(Post.draft == False)
    
    if "user" in include:
        query = query.options(joinedload(Post.user))
    if "tags" in include:
        query = query.options(joinedload(Post.tags))
    
    return query.all()

def get_post_by_id(db: Session, post_id: int, include: Optional[List[str]] = None):
    query = db.query(Post).filter(Post.id == post_id)

    if include:
        if 'tags' in include:
            query = query.options(joinedload(Post.tags))
        if 'user' in include:
            query = query.options(joinedload(Post.user))
        if 'comments' in include:
            query = query.options(joinedload(Post.comments))

    return query.first()


def create_post(db: Session, post: schemas.PostCreate):
    db_post = Post(
        id=post.id,
        post_text=post.post_text,
        draft=post.draft,
        user_id=post.user_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post



def get_user_by_id(db: Session, user_id: int, include: Optional[List[str]] = None):
    query = db.query(User).filter(User.id == user_id)

    if include:
        if 'posts' in include:
            query = query.options(joinedload(User.posts))
        if 'comments' in include:
            query = query.options(joinedload(User.comments))

    return query.first()


def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = Comment(
        id=comment.id,
        comment_text=comment.comment_text,
        post_id=comment.post_id,
        user_id=comment.user_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
