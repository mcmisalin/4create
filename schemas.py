from pydantic import BaseModel, ConfigDict
from typing import List, Optional, ClassVar



# Schema for Comment
class CommentBase(BaseModel):
    id: int
    text: str
    post_id: int
    user_id: int

    config: ClassVar[ConfigDict] = ConfigDict(orm_mode=True)
        

# Schema for Tag
class TagBase(BaseModel):
    id: int
    tag_name: str

    config: ClassVar[ConfigDict] = ConfigDict(orm_mode=True)


class TagCreate(TagBase):
    pass


# Schema for Post
class PostBase(BaseModel):
    id: int
    text: str
    draft: bool
    tags: List[TagBase] = [] 

    config: ClassVar[ConfigDict] = ConfigDict(orm_mode=True)


# Schema for User
class UserBase(BaseModel):
    id: int
    username: str
    posts: List[PostBase] = []  # To include posts
    comments: List[CommentBase] = []  # To include comments

    config: ClassVar[ConfigDict] = ConfigDict(orm_mode=True)


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
    text: str
    draft: bool
    user_id: int
    tag_ids: List[int]

class PostOut(PostBase):
    user: Optional[UserBase]
    comments: Optional[List['CommentOut']] = []
    tags: Optional[List['TagOut']] = []




class CommentCreate(CommentBase):
    text: str
    post_id: int
    user_id: int

class CommentOut(CommentBase):
    user: Optional[UserBase]
    post: Optional[PostBase]



