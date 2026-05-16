"""
管理员后台 API 路由
提供用户管理、内容管理、数据统计等功能
"""
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Optional, List

from ..database import get_db
from .. import models, schemas
from ..auth import (
    authenticate_admin,
    create_admin_token,
    verify_admin_token,
)

router = APIRouter(prefix="/admin", tags=["管理员"])


def get_admin_token(x_admin_token: Optional[str] = Header(None)) -> str:
    """获取并验证管理员Token"""
    if not x_admin_token:
        raise HTTPException(
            status_code=401,
            detail="缺少管理员Token，请先登录"
        )
    if not verify_admin_token(x_admin_token):
        raise HTTPException(
            status_code=401,
            detail="Token无效或已过期"
        )
    return x_admin_token


def require_admin(
    x_admin_token: str = Depends(get_admin_token),
    db: Session = Depends(get_db)
) -> dict:
    """验证管理员身份"""
    # Token验证已在get_admin_token中完成
    return {"username": "admin"}


# ============ 管理员登录 ============

@router.post("/login", response_model=schemas.AdminLoginResponse)
def admin_login(request: schemas.AdminLoginRequest, db: Session = Depends(get_db)):
    """管理员登录"""
    if not authenticate_admin(request.username, request.password, db):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    token = create_admin_token()
    return {
        "access_token": token,
        "token_type": "bearer",
        "is_admin": True
    }


@router.post("/logout")
def admin_logout(token: str = Depends(get_admin_token)):
    """管理员登出"""
    from ..auth import _admin_token_cache
    if token in _admin_token_cache:
        del _admin_token_cache[token]
    return {"message": "已退出登录"}


# ============ 数据统计 ============

@router.get("/stats", response_model=schemas.AdminStatsResponse)
def get_stats(
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取平台统计数据"""
    # 用户统计
    total_users = db.query(models.User).count()
    verified_users = db.query(models.User).filter(
        models.User.is_verified == True
    ).count()

    # 内容统计
    total_games = db.query(models.Game).count()
    total_articles = db.query(models.Article).count()
    total_comments = db.query(models.Comment).count()

    # 真实浏览量统计（使用 PageView 表）
    total_views = db.query(models.PageView).count()
    
    # 如果 PageView 表为空，使用旧的 Article.views + Game.views 作为后备
    if total_views == 0:
        article_views = db.query(models.Article).with_entities(
            func.sum(models.Article.views)
        ).scalar() or 0
        game_views = db.query(models.Game).with_entities(
            func.sum(models.Game.views)
        ).scalar() or 0
        total_views = article_views + game_views

    # 今日浏览量（真实数据）
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_views = db.query(models.PageView).filter(
        models.PageView.created_at >= today
    ).count()

    # 最近7天统计（真实数据）
    week_ago = datetime.now() - timedelta(days=7)
    recent_views = db.query(models.PageView).filter(
        models.PageView.created_at >= week_ago
    ).count()
    recent_articles = db.query(models.Article).filter(
        models.Article.created_at >= week_ago
    ).count()
    recent_comments = db.query(models.Comment).filter(
        models.Comment.created_at >= week_ago
    ).count()
    new_games = db.query(models.Game).filter(
        models.Game.created_at >= week_ago
    ).count()

    return {
        "total_users": total_users,
        "total_games": total_games,
        "total_articles": total_articles,
        "total_comments": total_comments,
        "total_views": total_views,
        "today_views": today_views,
        "verified_users": verified_users,
        "recent_articles": recent_articles,
        "recent_comments": recent_comments,
        "recent_views": recent_views,
        "new_games": new_games
    }


# ============ 用户管理 ============

@router.get("/users", response_model=List[schemas.UserManagementResponse])
def list_users(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取用户列表"""
    query = db.query(models.User)

    if search:
        query = query.filter(
            (models.User.username.like(f"%{search}%")) |
            (models.User.email.like(f"%{search}%"))
        )

    users = query.order_by(models.User.created_at.desc()).offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}", response_model=schemas.UserManagementResponse)
def get_user(
    user_id: int,
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取用户详情"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.put("/users/{user_id}/toggle-admin")
def toggle_user_admin(
    user_id: int,
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """切换用户管理员权限"""
    if user_id == 1:  # 防止修改第一个管理员
        raise HTTPException(status_code=400, detail="无法修改初始管理员权限")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    user.is_admin = not user.is_admin
    db.commit()
    return {"message": f"管理员权限已{'开启' if user.is_admin else '关闭'}"}


@router.put("/users/{user_id}/toggle-active")
def toggle_user_active(
    user_id: int,
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """切换用户激活状态"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    user.is_active = not user.is_active
    db.commit()
    return {"message": f"用户已{'启用' if user.is_active else '禁用'}"}


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """删除用户"""
    if user_id == 1:  # 防止删除第一个管理员
        raise HTTPException(status_code=400, detail="无法删除初始管理员")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 删除用户的文章和评论
    db.query(models.Comment).filter(models.Comment.author_id == user_id).delete()
    db.query(models.Article).filter(models.Article.author_id == user_id).delete()
    db.delete(user)
    db.commit()

    return {"message": "用户已删除"}


# ============ 游戏管理 ============

@router.get("/games", response_model=List[schemas.GameManagementResponse])
def list_games(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取游戏列表"""
    query = db.query(models.Game)

    if search:
        query = query.filter(
            (models.Game.name.like(f"%{search}%")) |
            (models.Game.developer.like(f"%{search}%"))
        )

    games = query.order_by(models.Game.created_at.desc()).offset(skip).limit(limit).all()
    return games


@router.post("/games", response_model=schemas.GameResponse)
def create_game(
    game: schemas.GameCreate,
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """创建游戏"""
    # 检查slug是否已存在
    existing = db.query(models.Game).filter(models.Game.slug == game.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="该slug已被使用")

    db_game = models.Game(**game.model_dump())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


@router.put("/games/{game_id}", response_model=schemas.GameResponse)
def update_game(
    game_id: int,
    game: schemas.GameCreate,
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """更新游戏"""
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="游戏不存在")

    # 检查slug是否与其他游戏冲突
    existing = db.query(models.Game).filter(
        models.Game.slug == game.slug,
        models.Game.id != game_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="该slug已被其他游戏使用")

    for key, value in game.model_dump().items():
        setattr(db_game, key, value)

    db.commit()
    db.refresh(db_game)
    return db_game


@router.delete("/games/{game_id}")
def delete_game(
    game_id: int,
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """删除游戏"""
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")

    # 删除关联的角色和文章
    db.query(models.Character).filter(models.Character.game_id == game_id).delete()
    db.query(models.Article).filter(models.Article.game_id == game_id).delete()
    db.delete(game)
    db.commit()

    return {"message": "游戏已删除"}


# ============ 文章管理 ============

@router.get("/articles", response_model=List[schemas.ArticleManagementResponse])
def list_articles(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    category: Optional[str] = None,
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取文章列表"""
    query = db.query(models.Article, models.User.username.label("author_username")).join(
        models.User, models.Article.author_id == models.User.id
    )

    if search:
        query = query.filter(models.Article.title.like(f"%{search}%"))

    if category:
        query = query.filter(models.Article.category == category)

    results = query.order_by(models.Article.created_at.desc()).offset(skip).limit(limit).all()

    # 转换为响应格式
    articles = []
    for article, username in results:
        articles.append({
            "id": article.id,
            "title": article.title,
            "slug": article.slug,
            "category": article.category,
            "views": article.views,
            "likes": article.likes,
            "is_published": article.is_published,
            "created_at": article.created_at,
            "author_username": username
        })
    return articles


@router.put("/articles/{article_id}/toggle-published")
def toggle_article_published(
    article_id: int,
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """切换文章发布状态"""
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    article.is_published = not article.is_published
    db.commit()
    return {"message": f"文章已{'发布' if article.is_published else '下架'}"}


@router.delete("/articles/{article_id}")
def delete_article(
    article_id: int,
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """删除文章"""
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    # 删除关联的评论
    db.query(models.Comment).filter(models.Comment.article_id == article_id).delete()
    db.delete(article)
    db.commit()

    return {"message": "文章已删除"}


# ============ 排行榜数据 ============

@router.get("/rankings/games")
def get_top_games(
    limit: int = 5,
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取游戏浏览排行榜"""
    games = db.query(models.Game).order_by(
        models.Game.views.desc()
    ).limit(limit).all()
    
    return [
        {
            "id": game.id,
            "name": game.name,
            "slug": game.slug,
            "views": game.views,
            "category": game.category
        }
        for game in games
    ]


@router.get("/rankings/articles")
def get_top_articles(
    limit: int = 5,
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取文章浏览排行榜"""
    articles = db.query(models.Article).filter(
        models.Article.is_published == True
    ).order_by(
        models.Article.views.desc()
    ).limit(limit).all()
    
    return [
        {
            "id": article.id,
            "title": article.title,
            "slug": article.slug,
            "views": article.views,
            "category": article.category
        }
        for article in articles
    ]


@router.get("/rankings/categories")
def get_article_categories(
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取文章分类统计（真实数据）"""
    # 按分类统计文章数量
    category_stats = db.query(
        models.Article.category,
        func.count(models.Article.id).label("count")
    ).filter(
        models.Article.is_published == True
    ).group_by(
        models.Article.category
    ).all()
    
    total_articles = sum(stat[1] for stat in category_stats)
    
    # 定义分类颜色
    category_colors = {
        "guide": "#667eea",
        "攻略": "#667eea",
        "news": "#4facfe",
        "新闻": "#4facfe",
        "review": "#f5576c",
        "评测": "#f5576c",
        "video": "#43e97b",
        "视频": "#43e97b",
        "community": "#ffb900",
        "社区": "#ffb900"
    }
    
    # 计算百分比
    categories = []
    for category, count in category_stats:
        percentage = round((count / total_articles * 100), 1) if total_articles > 0 else 0
        categories.append({
            "name": category,
            "value": percentage,
            "count": count,
            "color": category_colors.get(category, "#909399")
        })
    
    # 按数量排序
    categories.sort(key=lambda x: x["count"], reverse=True)
    
    return categories


@router.post("/analytics/cleanup")
def cleanup_analytics_data(
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    清理异常浏览数据
    - 移除同一IP在1分钟内对同一页面的重复记录（保留第一条）
    - 仅保留有效路径的记录
    """
    from datetime import timedelta
    
    # 获取1分钟内的记录用于去重
    one_minute_ago = datetime.now() - timedelta(minutes=1)
    
    # 查找并删除异常重复记录
    # 策略：保留每组 (ip_hash, path) 在1分钟内的第一条记录
    deleted_count = 0
    
    # 获取所有在1分钟内有重复的记录
    duplicates = db.query(
        models.PageView.id,
        models.PageView.ip_hash,
        models.PageView.path,
        models.PageView.created_at
    ).filter(
        models.PageView.created_at >= one_minute_ago
    ).order_by(
        models.PageView.created_at.asc()
    ).all()
    
    if duplicates:
        # 按 (ip_hash, path) 分组，保留第一条
        seen = {}
        to_delete = []
        
        for record in duplicates:
            key = (record[1], record[2])  # (ip_hash, path)
            if key in seen:
                to_delete.append(record[0])  # 保留后面的，删除前面的
            else:
                seen[key] = record[0]
        
        if to_delete:
            db.query(models.PageView).filter(
                models.PageView.id.in_(to_delete)
            ).delete(synchronize_session=False)
            deleted_count = len(to_delete)
    
    # 清理无效路径的记录（如空路径、测试路径）
    invalid_paths = ['/', '', None, '/api', '/favicon.ico', '/health']
    deleted_count += db.query(models.PageView).filter(
        models.PageView.path.in_(invalid_paths)
    ).delete(synchronize_session=False)
    
    db.commit()
    
    # 重新计算并修正 Game 和 Article 的 views 字段
    for game in db.query(models.Game).all():
        actual_views = db.query(models.PageView).filter(
            models.PageView.content_type == "game",
            models.PageView.content_id == game.id
        ).count()
        if game.views != actual_views:
            game.views = actual_views
    
    for article in db.query(models.Article).all():
        actual_views = db.query(models.PageView).filter(
            models.PageView.content_type == "article",
            models.PageView.content_id == article.id
        ).count()
        if article.views != actual_views:
            article.views = actual_views
    
    db.commit()
    
    return {
        "message": "数据清理完成",
        "deleted_duplicates": deleted_count
    }


@router.get("/analytics/verify")
def verify_analytics_data(
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    验证浏览数据准确性
    """
    # 统计概览
    total_page_views = db.query(models.PageView).count()
    
    # 游戏浏览统计
    game_views = db.query(models.PageView).filter(
        models.PageView.content_type == "game"
    ).count()
    
    # 文章浏览统计
    article_views = db.query(models.PageView).filter(
        models.PageView.content_type == "article"
    ).count()
    
    # 独立访客
    unique_visitors = db.query(models.PageView.ip_hash).distinct().count()
    
    # 独立会话
    unique_sessions = db.query(models.PageView.session_id).distinct().count()
    
    # 游戏表的浏览数总计
    game_table_views = db.query(func.sum(models.Game.views)).scalar() or 0
    
    # 文章表的浏览数总计
    article_table_views = db.query(func.sum(models.Article.views)).scalar() or 0
    
    return {
        "page_view_records": total_page_views,
        "game_page_views": game_views,
        "article_page_views": article_views,
        "unique_visitors": unique_visitors,
        "unique_sessions": unique_sessions,
        "game_table_total_views": game_table_views,
        "article_table_total_views": article_table_views,
        "data_match": (game_views == game_table_views and article_views == article_table_views)
    }


@router.get("/rankings/trend")
def get_views_trend(
    days: int = 7,
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取浏览量趋势数据（真实数据）"""
    trend_data = []
    now = datetime.now()
    
    for i in range(days - 1, -1, -1):
        date = now - timedelta(days=i)
        day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # 真实浏览量：查询当天PageView记录数
        daily_views = db.query(models.PageView).filter(
            models.PageView.created_at >= day_start,
            models.PageView.created_at <= day_end
        ).count()
        
        trend_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "views": daily_views
        })
    
    return trend_data


# ============ 评论管理 ============

@router.get("/comments")
def list_comments(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取评论列表"""
    query = db.query(models.Comment).options(
        joinedload(models.Comment.author),
        joinedload(models.Comment.article)
    )

    if search:
        query = query.filter(models.Comment.content.like(f"%{search}%"))

    total = query.count()
    
    comments = query.order_by(models.Comment.created_at.desc()).offset(skip).limit(limit).all()
    
    # 获取唯一用户数
    unique_users = db.query(models.Comment.author_id).distinct().count()
    
    # 为每个评论添加回复数
    result = []
    for comment in comments:
        comment_dict = {
            "id": comment.id,
            "content": comment.content,
            "likes": comment.likes,
            "created_at": comment.created_at,
            "author": {
                "id": comment.author.id,
                "username": comment.author.username
            } if comment.author else None,
            "article": {
                "id": comment.article.id,
                "title": comment.article.title
            } if comment.article else None,
            "reply_count": db.query(models.Comment).filter(
                models.Comment.parent_id == comment.id
            ).count()
        }
        result.append(comment_dict)
    
    return {
        "comments": result,
        "total": total,
        "unique_users": unique_users
    }


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    admin: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """删除评论"""
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="评论不存在")

    # 删除评论的所有回复
    db.query(models.Comment).filter(models.Comment.parent_id == comment_id).delete()
    db.delete(comment)
    db.commit()

    return {"message": "评论已删除"}
