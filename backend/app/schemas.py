from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List, TypeVar, Generic
from datetime import datetime


# ============ User Schemas ============
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    code: str  # 邮箱验证码
    birth_date: Optional[str] = None  # 出生日期 YYYY-MM-DD（年龄验证）


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class LoginWithVerifyRequest(BaseModel):
    email: EmailStr
    password: str
    turnstile_token: Optional[str] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None
    birth_date: Optional[str] = None  # YYYY-MM-DD


class UserResponse(BaseModel):
    id: int
    username: str
    email: str  # 使用 str 而非 EmailStr，避免数据库中已存在的旧邮箱（如 system.local）导致序列化失败
    avatar: str
    bio: Optional[str]
    birth_date: Optional[datetime] = None
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


# ============ Email Verification Schemas ============
class SendVerifyCodeRequest(BaseModel):
    email: EmailStr


class SendRegisterCodeRequest(BaseModel):
    email: EmailStr


class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: str


class SendVerifyCodeResponse(BaseModel):
    message: str
    expires_in: int = 300  # 验证码有效期（秒）


# ============ Password Change Schemas ============
class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str


class PasswordChangeResponse(BaseModel):
    message: str


# ============ Avatar Upload Schema ============
class AvatarUploadResponse(BaseModel):
    message: str
    avatar_url: str


# ============ Admin Schemas ============
class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    is_admin: bool = True


class AdminStatsResponse(BaseModel):
    total_users: int
    total_games: int
    total_articles: int
    total_comments: int
    total_views: int  # 总浏览量
    today_views: int  # 今日浏览
    verified_users: int
    recent_articles: int  # 最近7天的文章数
    recent_comments: int  # 最近7天的评论数
    recent_views: int  # 最近7天的浏览量
    new_games: int = 0  # 最近7天新增游戏数


class UserManagementResponse(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool
    is_verified: bool
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ArticleManagementResponse(BaseModel):
    id: int
    title: str
    slug: str
    category: str
    views: int
    likes: int
    is_published: bool
    created_at: datetime
    author_username: str

    model_config = ConfigDict(from_attributes=True)


class GameManagementResponse(BaseModel):
    id: int
    name: str
    slug: str
    category: str
    developer: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============ Hermes Agent API Schemas ============
class HermesAgentRequest(BaseModel):
    action: str  # search_games, get_articles, post_comment, etc.
    params: dict = {}


class HermesAgentResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None


# 向后兼容别名
OpenClawRequest = HermesAgentRequest
OpenClawResponse = HermesAgentResponse


# ============ Generic Pagination ============
T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int


# ============ Image Schemas ============
class ImageUploadResponse(BaseModel):
    id: int
    url: str
    filename: str
    original_name: str
    file_size: int
    mime_type: str
    width: Optional[int] = None
    height: Optional[int] = None
