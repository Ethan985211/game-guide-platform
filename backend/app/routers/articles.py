from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, desc
from typing import List, Optional

from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user

router = APIRouter(prefix="/articles", tags=["文章"])


@router.get("", response_model=List[schemas.ArticleResponse])
def get_articles(
    game_id: Optional[int] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    author_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(models.Article).filter(models.Article.is_published == True)

    if game_id:
        query = query.filter(models.Article.game_id == game_id)
    if category:
        query = query.filter(models.Article.category == category)
    if author_id:
        query = query.filter(models.Article.author_id == author_id)
    if search:
        query = query.filter(
            or_(
                models.Article.title.ilike(f"%{search}%"),
                models.Article.content.ilike(f"%{search}%"),
            )
        )

    return query.options(
        joinedload(models.Article.author),
        joinedload(models.Article.game)
    ).order_by(desc(models.Article.created_at)).offset(skip).limit(limit).all()


@router.get("/{article_id}", response_model=schemas.ArticleDetail)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = (
        db.query(models.Article)
        .options(
            joinedload(models.Article.author),
            joinedload(models.Article.game)
        )
        .filter(models.Article.id == article_id)
        .first()
    )
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    # 增加浏览量
    article.views += 1
    db.commit()

    return article


@router.post("", response_model=schemas.ArticleResponse)
def create_article(
    article: schemas.ArticleCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # 检查slug唯一性
    existing = db.query(models.Article).filter(models.Article.slug == article.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="文章slug已存在")

    db_article = models.Article(
        **article.model_dump(),
        author_id=current_user.id
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


@router.put("/{article_id}", response_model=schemas.ArticleResponse)
def update_article(
    article_id: int,
    article_update: schemas.ArticleUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="文章不存在")

    # 检查权限：作者或管理员
    if db_article.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="没有权限修改此文章")

    for key, value in article_update.model_dump(exclude_unset=True).items():
        setattr(db_article, key, value)

    db.commit()
    db.refresh(db_article)
    return db_article


@router.delete("/{article_id}")
def delete_article(
    article_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="文章不存在")

    if db_article.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="没有权限删除此文章")

    db.delete(db_article)
    db.commit()
    return {"message": "文章已删除"}


@router.post("/{article_id}/like")
def like_article(
    article_id: int,
    db: Session = Depends(get_db),
):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    article.likes += 1
    db.commit()
    return {"likes": article.likes}
