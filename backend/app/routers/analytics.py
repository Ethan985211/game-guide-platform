"""
统计分析 API 路由
提供页面浏览追踪等功能，无需登录即可记录访问
"""
from fastapi import APIRouter, Request, Depends, Header
from fastapi.responses import Response
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
import hashlib
import uuid

from ..database import get_db
from .. import models

router = APIRouter(prefix="/analytics", tags=["统计分析"])


def get_client_ip(request: Request) -> str:
    """获取客户端IP并哈希处理"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        ip = forwarded.split(",")[0].strip()
    else:
        ip = request.client.host if request.client else "unknown"
    
    # 哈希处理以保护隐私
    return hashlib.sha256(ip.encode()).hexdigest()[:32]


@router.post("/track")
def track_page_view(
    request: Request,
    content_type: str = None,
    content_id: int = None,
    db: Session = Depends(get_db)
):
    """
    记录页面浏览
    - 无需认证，所有访客都会被记录
    - 使用IP哈希进行去重
    - 记录会话信息用于分析
    """
    # 获取请求信息
    path = str(request.url.path)
    referrer = request.headers.get("Referer", "")[:500] if request.headers.get("Referer") else None
    user_agent = request.headers.get("User-Agent", "")[:500] if request.headers.get("User-Agent") else None
    ip_hash = get_client_ip(request)
    
    # 生成或获取会话ID
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    
    # 创建浏览记录
    page_view = models.PageView(
        path=path,
        referrer=referrer,
        user_agent=user_agent,
        ip_hash=ip_hash,
        session_id=session_id,
        content_type=content_type,
        content_id=content_id
    )
    
    db.add(page_view)
    db.commit()
    
    # 同时更新对应内容的 views 计数
    if content_type == "game" and content_id:
        game = db.query(models.Game).filter(models.Game.id == content_id).first()
        if game:
            game.views += 1
            db.commit()
    elif content_type == "article" and content_id:
        article = db.query(models.Article).filter(models.Article.id == content_id).first()
        if article:
            article.views += 1
            db.commit()
    
    return {
        "success": True,
        "session_id": session_id
    }


@router.get("/summary")
def get_analytics_summary(
    days: int = 7,
    db: Session = Depends(get_db)
):
    """获取访问概览数据"""
    from datetime import timedelta
    
    now = datetime.now()
    start_date = now - timedelta(days=days)
    
    # 总浏览量
    total_views = db.query(models.PageView).count()
    
    # 指定时间段浏览量
    period_views = db.query(models.PageView).filter(
        models.PageView.created_at >= start_date
    ).count()
    
    # 独立访客数（基于IP哈希去重）
    unique_visitors = db.query(models.PageView.ip_hash).distinct().count()
    
    # 热门页面
    from sqlalchemy import func
    hot_pages_raw = db.query(
        models.PageView.path,
        func.count(models.PageView.id).label("count")
    ).group_by(
        models.PageView.path
    ).order_by(
        func.count(models.PageView.id).desc()
    ).limit(10).all()
    
    # SQLite 返回的是元组列表，需要正确访问
    hot_pages = [{"path": row[0], "views": row[1]} for row in hot_pages_raw]
    
    return {
        "total_views": total_views,
        "period_views": period_views,
        "unique_visitors": unique_visitors,
        "hot_pages": hot_pages,
        "period_days": days
    }


@router.post("/batch")
async def track_batch_views(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    批量记录页面浏览（用于前端队列发送）
    """
    try:
        body = await request.json()
        views_data = body.get("views", [])
        
        if not views_data:
            return {"success": True, "count": 0}
        
        client_ip = request.client.host if request.client else "unknown"
        ip_hash = hashlib.sha256(client_ip.encode()).hexdigest()[:32]
        
        for view in views_data:
            page_view = models.PageView(
                path=view.get("path", "/"),
                referrer=view.get("referrer"),
                user_agent=view.get("user_agent"),
                ip_hash=ip_hash,
                session_id=view.get("session_id", str(uuid.uuid4())),
                content_type=view.get("content_type"),
                content_id=view.get("content_id")
            )
            db.add(page_view)
            
            # 更新内容浏览数
            content_type = view.get("content_type")
            content_id = view.get("content_id")
            
            if content_type == "game" and content_id:
                game = db.query(models.Game).filter(models.Game.id == content_id).first()
                if game:
                    game.views += 1
            elif content_type == "article" and content_id:
                article = db.query(models.Article).filter(models.Article.id == content_id).first()
                if article:
                    article.views += 1
        
        db.commit()
        return {"success": True, "count": len(views_data)}
        
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}
