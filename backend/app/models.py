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
