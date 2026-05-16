from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user

router = APIRouter(prefix="/comments", tags=["评论"])


@router.get("/article/{article_id}", response_model=List[schemas.CommentDetail])
def get_article_comments(article_id: int, db: Session = Depends(get_db)):
    # 获取顶级评论（parent_id为空的评论）
    comments = (
        db.query(models.Comment)
        .options(joinedload(models.Comment.author))
        .filter(
            models.Comment.article_id == article_id,
            models.Comment.parent_id == None
        )
        .order_by(models.Comment.created_at.desc())
        .all()
    )

    # 加载回复
    for comment in comments:
        comment.replies = (
            db.query(models.Comment)
            .options(joinedload(models.Comment.author))
            .filter(models.Comment.parent_id == comment.id)
            .order_by(models.Comment.created_at.asc())
            .all()
        )

    return comments


@router.post("", response_model=schemas.CommentResponse)
def create_comment(
    comment: schemas.CommentCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # 检查文章是否存在
    article = db.query(models.Article).filter(models.Article.id == comment.article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    # 如果有parent_id，检查父评论是否存在
    if comment.parent_id:
        parent = db.query(models.Comment).filter(models.Comment.id == comment.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="父评论不存在")
        if parent.article_id != comment.article_id:
            raise HTTPException(status_code=400, detail="父评论不属于该文章")

    db_comment = models.Comment(
        **comment.model_dump(),
        author_id=current_user.id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="评论不存在")

    if db_comment.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="没有权限删除此评论")

    db.delete(db_comment)
    db.commit()
    return {"message": "评论已删除"}


@router.post("/{comment_id}/like")
def like_comment(
    comment_id: int,
    db: Session = Depends(get_db),
):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="评论不存在")

    comment.likes += 1
    db.commit()
    return {"likes": comment.likes}
