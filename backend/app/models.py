from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    avatar = Column(String(500), default="/static/avatars/default.png")
    bio = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)  # 邮箱是否已验证
    verification_code = Column(String(6), nullable=True)  # 验证码
    verification_expires = Column(DateTime(timezone=True), nullable=True)  # 验证码过期时间
    birth_date = Column(DateTime, nullable=True, default=None)  # 出生日期（年龄验证）
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    articles = relationship("Article", back_populates="author")
    comments = relationship("Comment", back_populates="author")


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    slug = Column(String(100), unique=True, index=True)
    cover_image = Column(String(500))
    description = Column(Text)
    category = Column(String(50))  # RPG, FPS, MOBA, etc.
    release_date = Column(DateTime, nullable=True)
    developer = Column(String(100))
    publisher = Column(String(100))
    views = Column(Integer, default=0)  # 游戏页面浏览量
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    characters = relationship("Character", back_populates="game")
    articles = relationship("Article", back_populates="game")


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    name = Column(String(100), index=True)
    rarity = Column(String(20), nullable=True)  # 角色稀有度
    element = Column(String(30), nullable=True)  # 元素属性
    weapon_type = Column(String(30), nullable=True)  # 武器类型
    description = Column(Text)
    image = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    game = relationship("Game", back_populates="characters")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    slug = Column(String(200), unique=True, index=True)
    content = Column(Text)
    cover_image = Column(String(500), nullable=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String(50), default="guide")  # guide, news, tips
    tags = Column(String(200), nullable=True)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    author = relationship("User", back_populates="articles")
    game = relationship("Game", back_populates="articles")
    comments = relationship("Comment", back_populates="article")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    article_id = Column(Integer, ForeignKey("articles.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    likes = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    article = relationship("Article", back_populates="comments")
    author = relationship("User", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")


class AdminUser(Base):
    """管理员用户表"""
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password_hash = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PageView(Base):
    """页面浏览记录表 - 用于追踪真实访问数据"""
    __tablename__ = "page_views"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String(500), index=True)  # 页面路径
    referrer = Column(String(500), nullable=True)  # 来源页面
    user_agent = Column(String(500), nullable=True)  # 用户代理
    ip_hash = Column(String(64), nullable=True)  # IP哈希（用于去重，不存储真实IP）
    session_id = Column(String(64), index=True)  # 会话ID
    content_type = Column(String(50), nullable=True)  # 内容类型: game, article, home
    content_id = Column(Integer, nullable=True)  # 内容ID
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)


class ArticleImage(Base):
    """文章图片表 - 文章内嵌图片"""
    __tablename__ = "article_images"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=True)  # nullable 因为上传时可未关联文章
    filename = Column(String(255))  # 存储的文件名
    original_name = Column(String(255))  # 原始文件名
    file_size = Column(Integer)  # 文件大小（字节）
    mime_type = Column(String(50))  # MIME 类型
    width = Column(Integer, nullable=True)  # 图片宽度
    height = Column(Integer, nullable=True)  # 图片高度
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    article = relationship("Article", backref="images")
    uploader = relationship("User")
