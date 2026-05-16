from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/search", tags=["搜索"])


@router.get("")
def search(
    q: str = Query(..., min_length=1),
    type: Optional[str] = None,  # games, articles, characters, all
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    results = {"games": [], "articles": [], "characters": []}
    search_pattern = f"%{q}%"

    # 搜索游戏
    if not type or type == "games" or type == "all":
        games = db.query(models.Game).filter(
            or_(
                models.Game.name.ilike(search_pattern),
                models.Game.description.ilike(search_pattern),
            )
        ).offset(skip).limit(limit).all()
        results["games"] = games

    # 搜索文章
    if not type or type == "articles" or type == "all":
        articles = db.query(models.Article).filter(
            models.Article.is_published == True,
            or_(
                models.Article.title.ilike(search_pattern),
                models.Article.content.ilike(search_pattern),
            )
        ).offset(skip).limit(limit).all()
        results["articles"] = articles

    # 搜索角色
    if not type or type == "characters" or type == "all":
        characters = db.query(models.Character).filter(
            or_(
                models.Character.name.ilike(search_pattern),
                models.Character.description.ilike(search_pattern),
            )
        ).offset(skip).limit(limit).all()
        results["characters"] = characters

    return results
