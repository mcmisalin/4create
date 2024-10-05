from typing import List, Optional
from uuid import UUID
from sqlalchemy import insert
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from models import Post, User, Comment, Tag, post_tags
import schemas

def seed_initial_data(db: Session):
    if db.query(User).count() == 0:
        db.add_all([
            User(username='milos'),
            User(username='jasmina'),
            User(username='oleg')
        ])
        db.commit()

    if db.query(Tag).count() == 0:
        db.add_all([
            Tag(name='dev'),
            Tag(name='hr'),
            Tag(name='mentor')
        ])
        db.commit()


    if db.query(Post).count() == 0:
        user1 = db.query(User).filter(User.username == 'milos').first()
        user2 = db.query(User).filter(User.username == 'jasmina').first()
        user3 = db.query(User).filter(User.username == 'oleg').first()

        
        post1 = Post(text='Post about padel', draft=False, user_id=user1.id)
        post2 = Post(text='Second post about golf', draft=True, user_id=user2.id)
        post3 = Post(text='Third post about 4create', draft=False, user_id=user3.id)
        
        db.add_all([post1, post2, post3])
        db.commit()

        dev_tag = db.query(Tag).filter_by(name="dev").first()
        hr_tag = db.query(Tag).filter_by(name="hr").first()
        mentor_tag = db.query(Tag).filter_by(name="mentor").first()
        
        post_tag1 = insert(post_tags).values(post_id=post1.id, tag_id=dev_tag.id)
        post_tag2 = insert(post_tags).values(post_id=post2.id, tag_id=hr_tag.id)
        post_tag3 = insert(post_tags).values(post_id=post1.id, tag_id=mentor_tag.id)
        post_tag4 = insert(post_tags).values(post_id=post3.id, tag_id=hr_tag.id)
        post_tag5 = insert(post_tags).values(post_id=post2.id, tag_id=dev_tag.id)
            
        db.execute(post_tag1)
        db.execute(post_tag2)
        db.execute(post_tag3)
        db.execute(post_tag4)
        db.execute(post_tag5)
        db.commit()

        
        comment1 = Comment(text='Great post on padel!', post_id=post1.id, user_id=user1.id)
        comment2 = Comment(text='Very informative, thanks for sharing!', post_id=post2.id,user_id=user2.id)
        comment3 = Comment(text='I dig padel!', post_id=post1.id, user_id=user1.id)
        comment4 = Comment(text='Looking forward to more posts about golf.', post_id=post2.id, user_id=user2.id)
        comment5= Comment(text='Mentor thinks is good.', post_id=post2.id, user_id=user3.id)
        comment6 = Comment(text='HR approves!.', post_id=post3.id, user_id=user2.id)

        db.add_all([comment1, comment2, comment3, comment4, comment5, comment6])
        
        db.commit()


def get_posts(db: Session, status: str = None, include: list = []):
    query = db.query(Post)
    
    if status:
        if status == "draft":
            query = query.filter(Post.draft == True)
        elif status == "published":
            query = query.filter(Post.draft == False)
    print(f"include: {include}")
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
        text=post.text,
        draft=post.draft,
        user_id=post.user_id
    )
    db.add(db_post)
    db.commit()
    
    for tag_id in post.tag_ids:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if tag:
            db_post.tags.append(tag)
            
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
        text=comment.text,
        post_id=comment.post_id,
        user_id=comment.user_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
