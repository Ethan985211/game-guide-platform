from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user

router = APIRouter(prefix="/games", tags=["游戏"])


@router.get("", response_model=List[schemas.GameResponse])
def get_games(
    category: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(models.Game)

    if category:
        query = query.filter(models.Game.category == category)

    if search:
        query = query.filter(
            or_(
                models.Game.name.ilike(f"%{search}%"),
                models.Game.description.ilike(f"%{search}%"),
            )
        )

    return query.order_by(models.Game.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{game_id}", response_model=schemas.GameResponse)
def get_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")
    
    # 增加游戏浏览量
    game.views += 1
    db.commit()
    
    return game


@router.get("/{game_id}/characters", response_model=List[schemas.CharacterResponse])
def get_game_characters(game_id: int, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")
    return db.query(models.Character).filter(models.Character.game_id == game_id).all()


@router.post("", response_model=schemas.GameResponse)
def create_game(
    game: schemas.GameCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")

    existing = db.query(models.Game).filter(models.Game.slug == game.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="游戏slug已存在")

    db_game = models.Game(**game.model_dump())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


@router.put("/{game_id}", response_model=schemas.GameResponse)
def update_game(
    game_id: int,
    game_update: schemas.GameCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")

    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="游戏不存在")

    for key, value in game_update.model_dump().items():
        setattr(db_game, key, value)

    db.commit()
    db.refresh(db_game)
    return db_game
