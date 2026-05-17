"""
爬虫内容导入 API — 使用 API Key 认证，供外部爬虫推送文章和更新游戏信息
"""
import os
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from ..database import get_db
from .. import models

router = APIRouter(prefix="/crawler", tags=["爬虫"])

CRAWLER_API_KEY = os.getenv("CRAWLER_API_KEY", "crawler-secret-key-change-me")


def verify_crawler(x_api_key: str = Header(None)) -> str:
    if not x_api_key or x_api_key != CRAWLER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


class ArticleImport(BaseModel):
    title: str
    slug: str
    content: str
    game_id: Optional[int] = None
    category: str = "news"
    tags: Optional[str] = None
    cover_image: Optional[str] = None


class GameInfoUpdate(BaseModel):
    description: Optional[str] = None
    developer: Optional[str] = None
    publisher: Optional[str] = None
    release_date: Optional[str] = None
    cover_image: Optional[str] = None
    category: Optional[str] = None


@router.post("/articles")
def import_articles(
    articles: List[ArticleImport],
    x_api_key: str = Depends(verify_crawler),
    db: Session = Depends(get_db),
):
    """批量导入文章。slug 重复的跳过。author_id 用系统用户(1)"""
    created = 0
    skipped = 0
    for art in articles:
        existing = db.query(models.Article).filter(models.Article.slug == art.slug).first()
        if existing:
            skipped += 1
            continue
        db_article = models.Article(
            **art.model_dump(),
            author_id=1,
            is_published=True,
        )
        db.add(db_article)
        created += 1
    db.commit()
    return {"created": created, "skipped": skipped}


@router.patch("/games/{game_id}")
def update_game_info(
    game_id: int,
    info: GameInfoUpdate,
    x_api_key: str = Depends(verify_crawler),
    db: Session = Depends(get_db),
):
    """更新游戏元数据"""
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")
    for key, value in info.model_dump(exclude_unset=True).items():
        if value is not None:
            if key == "release_date" and isinstance(value, str):
                parsed = None
                # Try multiple date formats
                formats = [
                    lambda v: datetime.fromisoformat(v.replace("Z", "+00:00")),
                    lambda v: datetime.strptime(v, "%d %b, %Y"),
                    lambda v: datetime.strptime(v, "%b %d, %Y"),
                    lambda v: datetime.strptime(v, "%d %B, %Y"),
                    lambda v: datetime.strptime(v, "%B %d, %Y"),
                    lambda v: datetime.strptime(v, "%Y-%m-%d"),
                    lambda v: datetime.strptime(v, "%Y年%m月%d日"),
                ]
                for fmt in formats:
                    try:
                        parsed = fmt(value)
                        break
                    except (ValueError, TypeError):
                        continue
                if parsed is None:
                    continue  # skip if unparseable
                value = parsed
            setattr(game, key, value)
    db.commit()
    return {"ok": True}
