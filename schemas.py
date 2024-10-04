from pydantic import BaseModel
from typing import List, Optional

# Schema for Comment
class CommentBase(BaseModel):
    id: int
    comment_text: str
    post_id: int
    user_id: int

    class Config:
        from_attributes = True
        

# Schema for Tag
class TagBase(BaseModel):
    id: int
    tag_name: str

    class Config:
        from_attributes = True

class TagCreate(TagBase):
    pass


# Schema for Post
class PostBase(BaseModel):
    id: int
    post_text: str
    draft: bool
    tags: List[TagBase] = [] 

    class Config:
        from_attributes = True

# Schema for User
class UserBase(BaseModel):
    id: int
    username: str
    posts: List[PostBase] = []  # To include posts
    comments: List[CommentBase] = []  # To include comments

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    pass

class UserWithPosts(UserBase):
    posts: List['PostOut'] = []

class UserWithComments(UserBase):
    comments: List['CommentOut'] = []

class UserOut(UserBase):
    posts: Optional[List['PostOut']] = []
    comments: Optional[List['CommentOut']] = []




class TagOut(TagBase):
    posts: Optional[List[PostBase]] = []

class PostCreate(PostBase):
    user_id: int

class PostOut(PostBase):
    user: Optional[UserBase]
    comments: Optional[List['CommentOut']] = []
    tags: Optional[List['TagOut']] = []




class CommentCreate(CommentBase):
    pass

class CommentOut(CommentBase):
    user: Optional[UserBase]
    post: Optional[PostBase]



