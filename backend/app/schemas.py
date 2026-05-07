from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime


# ============ User Schemas ============
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None


class UserResponse(UserBase):
    id: int
    avatar: str
    bio: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============ Game Schemas ============
class GameBase(BaseModel):
    name: str
    slug: str
    description: str
    category: str
    developer: str
    publisher: str


class GameCreate(GameBase):
    cover_image: Optional[str] = None
    release_date: Optional[datetime] = None


class GameResponse(GameBase):
    id: int
    slug: str
    cover_image: Optional[str]
    release_date: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============ Character Schemas ============
class CharacterBase(BaseModel):
    name: str
    description: str
    rarity: Optional[str] = None
    element: Optional[str] = None
    weapon_type: Optional[str] = None


class CharacterCreate(CharacterBase):
    game_id: int
    image: Optional[str] = None


class CharacterResponse(CharacterBase):
    id: int
    game_id: int
    image: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============ Article Schemas ============
class ArticleBase(BaseModel):
    title: str
    slug: str
    content: str
    category: str = "guide"
    tags: Optional[str] = None


class ArticleCreate(ArticleBase):
    game_id: Optional[int] = None
    cover_image: Optional[str] = None


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    cover_image: Optional[str] = None
    is_published: Optional[bool] = None


class ArticleResponse(ArticleBase):
    id: int
    cover_image: Optional[str]
    game_id: Optional[int]
    author_id: int
    views: int
    likes: int
    is_published: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class ArticleDetail(ArticleResponse):
    author: UserResponse
    game: Optional[GameResponse] = None

    model_config = ConfigDict(from_attributes=True)


# ============ Comment Schemas ============
class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    article_id: int
    parent_id: Optional[int] = None


class CommentResponse(CommentBase):
    id: int
    article_id: int
    author_id: int
    parent_id: Optional[int]
    likes: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommentDetail(CommentResponse):
    author: UserResponse
    replies: List[CommentResponse] = []

    model_config = ConfigDict(from_attributes=True)


# ============ Auth Schemas ============
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None
