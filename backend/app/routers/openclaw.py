"""
OpenClaw 智能体 API 路由
为AI智能体提供游戏攻略平台数据访问接口
"""
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from .. import models, schemas
from ..auth import (
    verify_openclaw_api_key,
    get_openclaw_user,
)

router = APIRouter(prefix="/openclaw", tags=["OpenClaw智能体"])


def require_openclaw_api_key(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    db: Session = Depends(get_db)
):
    """验证OpenClaw API密钥"""
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="缺少API密钥，请提供 X-API-Key"
        )

    if not verify_openclaw_api_key(x_api_key):
        raise HTTPException(
            status_code=401,
            detail="API密钥无效"
        )

    return x_api_key


def get_openclaw_db_user(db: Session = Depends(get_db)):
    """获取OpenClaw系统用户"""
    return get_openclaw_user(db)


# ============ 智能体状态 ============

@router.get("/status")
def get_openclaw_status(
    api_key: str = Depends(require_openclaw_api_key),
    db: Session = Depends(get_db)
):
    """获取OpenClaw智能体状态"""
    return {
        "status": "online",
        "service": "Game Guide Platform",
        "version": "1.0.0",
        "capabilities": [
            "search_games",
            "get_game_details",
            "get_game_characters",
            "search_articles",
            "get_article_details",
            "create_comment",
            "get_platform_stats"
        ]
    }


# ============ 游戏搜索 ============

@router.get("/games/search")
def search_games(
    q: str,
    limit: int = 10,
    api_key: str = Depends(require_openclaw_api_key),
    db: Session = Depends(get_db)
):
    """搜索游戏"""
    games = db.query(models.Game).filter(
        (models.Game.name.like(f"%{q}%")) |
        (models.Game.developer.like(f"%{q}%")) |
        (models.Game.category.like(f"%{q}%"))
    ).limit(limit).all()

    return {
        "success": True,
        "data": {
            "games": [
                {
                    "id": g.id,
                    "name": g.name,
                    "slug": g.slug,
                    "category": g.category,
                    "developer": g.developer,
                    "cover_image": g.cover_image
                }
                for g in games
            ],
            "total": len(games)
        }
    }


@router.get("/games/{game_id}")
def get_game_details(
    game_id: int,
    api_key: str = Depends(require_openclaw_api_key),
    db: Session = Depends(get_db)
):
    """获取游戏详情"""
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")

    # 获取角色数量
    character_count = db.query(models.Character).filter(
        models.Character.game_id == game_id
    ).count()

    # 获取文章数量
    article_count = db.query(models.Article).filter(
        models.Article.game_id == game_id,
        models.Article.is_published == True
    ).count()

    return {
        "success": True,
        "data": {
            "id": game.id,
            "name": game.name,
            "slug": game.slug,
            "description": game.description,
            "category": game.category,
            "developer": game.developer,
            "publisher": game.publisher,
            "cover_image": game.cover_image,
            "release_date": game.release_date.isoformat() if game.release_date else None,
            "character_count": character_count,
            "article_count": article_count
        }
    }


# ============ 角色查询 ============

@router.get("/games/{game_id}/characters")
def get_game_characters(
    game_id: int,
    limit: int = 20,
    api_key: str = Depends(require_openclaw_api_key),
    db: Session = Depends(get_db)
):
    """获取游戏角色列表"""
    characters = db.query(models.Character).filter(
        models.Character.game_id == game_id
    ).limit(limit).all()

    return {
        "success": True,
        "data": {
            "characters": [
                {
                    "id": c.id,
                    "name": c.name,
                    "rarity": c.rarity,
                    "element": c.element,
                    "weapon_type": c.weapon_type,
                    "image": c.image
                }
                for c in characters
            ],
            "total": len(characters)
        }
    }


# ============ 文章查询 ============

@router.get("/articles/search")
def search_articles(
    q: str,
    game_id: Optional[int] = None,
    category: Optional[str] = None,
    limit: int = 10,
    api_key: str = Depends(require_openclaw_api_key),
    db: Session = Depends(get_db)
):
    """搜索文章"""
    query = db.query(models.Article).filter(
        models.Article.is_published == True,
        (models.Article.title.like(f"%{q}%")) |
        (models.Article.content.like(f"%{q}%")) |
        (models.Article.tags.like(f"%{q}%"))
    )

    if game_id:
        query = query.filter(models.Article.game_id == game_id)

    if category:
        query = query.filter(models.Article.category == category)

    articles = query.order_by(models.Article.views.desc()).limit(limit).all()

    return {
        "success": True,
        "data": {
            "articles": [
                {
                    "id": a.id,
                    "title": a.title,
                    "slug": a.slug,
                    "category": a.category,
                    "views": a.views,
                    "likes": a.likes,
                    "game_id": a.game_id,
                    "author_id": a.author_id
                }
                for a in articles
            ],
            "total": len(articles)
        }
    }


@router.get("/articles/{article_id}")
def get_article_details(
    article_id: int,
    api_key: str = Depends(require_openclaw_api_key),
    db: Session = Depends(get_db)
):
    """获取文章详情"""
    article = db.query(models.Article).filter(
        models.Article.id == article_id,
        models.Article.is_published == True
    ).first()

    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    # 获取作者信息
    author = db.query(models.User).filter(models.User.id == article.author_id).first()

    # 获取游戏信息
    game = None
    if article.game_id:
        game = db.query(models.Game).filter(models.Game.id == article.game_id).first()

    # 增加浏览量
    article.views += 1
    db.commit()

    return {
        "success": True,
        "data": {
            "id": article.id,
            "title": article.title,
            "slug": article.slug,
            "content": article.content,
            "category": article.category,
            "tags": article.tags,
            "views": article.views,
            "likes": article.likes,
            "cover_image": article.cover_image,
            "author": {
                "id": author.id,
                "username": author.username,
                "avatar": author.avatar
            } if author else None,
            "game": {
                "id": game.id,
                "name": game.name,
                "slug": game.slug
            } if game else None,
            "created_at": article.created_at.isoformat() if article.created_at else None
        }
    }


# ============ 评论操作 ============

@router.get("/articles/{article_id}/comments")
def get_article_comments(
    article_id: int,
    api_key: str = Depends(require_openclaw_api_key),
    db: Session = Depends(get_db)
):
    """获取文章评论"""
    comments = db.query(models.Comment).filter(
        models.Comment.article_id == article_id
    ).order_by(models.Comment.created_at.desc()).all()

    # 获取评论者信息
    result = []
    for comment in comments:
        author = db.query(models.User).filter(models.User.id == comment.author_id).first()
        result.append({
            "id": comment.id,
            "content": comment.content,
            "likes": comment.likes,
            "author": {
                "id": author.id,
                "username": author.username,
                "avatar": author.avatar
            } if author else None,
            "created_at": comment.created_at.isoformat() if comment.created_at else None
        })

    return {
        "success": True,
        "data": {
            "comments": result,
            "total": len(result)
        }
    }


@router.post("/comments")
def create_comment(
    comment: schemas.CommentCreate,
    api_key: str = Depends(require_openclaw_api_key),
    db_user = Depends(get_openclaw_db_user),
    db: Session = Depends(get_db)
):
    """创建评论（智能体专用）"""
    # 检查文章是否存在
    article = db.query(models.Article).filter(
        models.Article.id == comment.article_id
    ).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    # 创建评论
    db_comment = models.Comment(
        content=comment.content,
        article_id=comment.article_id,
        author_id=db_user.id,
        parent_id=comment.parent_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return {
        "success": True,
        "data": {
            "id": db_comment.id,
            "content": db_comment.content,
            "created_at": db_comment.created_at.isoformat() if db_comment.created_at else None
        }
    }


# ============ 平台统计 ============

@router.get("/stats")
def get_platform_stats(
    api_key: str = Depends(require_openclaw_api_key),
    db: Session = Depends(get_db)
):
    """获取平台统计数据"""
    from datetime import datetime, timedelta

    total_games = db.query(models.Game).count()
    total_articles = db.query(models.Article).filter(
        models.Article.is_published == True
    ).count()
    total_users = db.query(models.User).filter(
        models.User.is_active == True
    ).count()

    # 获取热门游戏（按文章数量排序）
    hot_games = db.query(
        models.Game,
        func.count(models.Article.id).label("article_count")
    ).join(
        models.Article, models.Game.id == models.Article.game_id
    ).group_by(
        models.Game.id
    ).order_by(
        func.count(models.Article.id).desc()
    ).limit(5).all()

    # 获取热门文章（按浏览量排序）
    hot_articles = db.query(models.Article).filter(
        models.Article.is_published == True
    ).order_by(
        models.Article.views.desc()
    ).limit(5).all()

    return {
        "success": True,
        "data": {
            "total_games": total_games,
            "total_articles": total_articles,
            "total_users": total_users,
            "hot_games": [
                {
                    "id": g.id,
                    "name": g.name,
                    "slug": g.slug,
                    "article_count": count
                }
                for g, count in hot_games
            ],
            "hot_articles": [
                {
                    "id": a.id,
                    "title": a.title,
                    "slug": a.slug,
                    "views": a.views,
                    "likes": a.likes
                }
                for a in hot_articles
            ]
        }
    }


# ============ 交互式问答 ============

@router.post("/query")
def ai_query(
    query_request: schemas.OpenClawRequest,
    api_key: str = Depends(require_openclaw_api_key),
    db: Session = Depends(get_db)
):
    """AI智能体查询接口"""
    action = query_request.action
    params = query_request.params

    if action == "search_games":
        return search_games(
            q=params.get("q", ""),
            limit=params.get("limit", 10),
            api_key=api_key,
            db=db
        )

    elif action == "get_game_details":
        return get_game_details(
            game_id=params.get("game_id"),
            api_key=api_key,
            db=db
        )

    elif action == "get_game_characters":
        return get_game_characters(
            game_id=params.get("game_id"),
            limit=params.get("limit", 20),
            api_key=api_key,
            db=db
        )

    elif action == "search_articles":
        return search_articles(
            q=params.get("q", ""),
            game_id=params.get("game_id"),
            category=params.get("category"),
            limit=params.get("limit", 10),
            api_key=api_key,
            db=db
        )

    elif action == "get_article_details":
        return get_article_details(
            article_id=params.get("article_id"),
            api_key=api_key,
            db=db
        )

    elif action == "get_platform_stats":
        return get_platform_stats(
            api_key=api_key,
            db=db
        )

    else:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的操作: {action}"
        )
