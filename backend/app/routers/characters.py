from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user
from .admin import verify_admin_token

router = APIRouter(prefix="/characters", tags=["角色"])


@router.get("", response_model=List[schemas.CharacterResponse])
def get_characters(
    game_id: Optional[int] = None,
    element: Optional[str] = None,
    weapon_type: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(models.Character)

    if game_id:
        query = query.filter(models.Character.game_id == game_id)
    if element:
        query = query.filter(models.Character.element == element)
    if weapon_type:
        query = query.filter(models.Character.weapon_type == weapon_type)
    if search:
        query = query.filter(models.Character.name.ilike(f"%{search}%"))

    return query.offset(skip).limit(limit).all()


@router.get("/{character_id}", response_model=schemas.CharacterResponse)
def get_character(character_id: int, db: Session = Depends(get_db)):
    character = db.query(models.Character).filter(models.Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="角色不存在")
    return character


@router.post("", response_model=schemas.CharacterResponse)
def create_character(
    character: schemas.CharacterCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")

    game = db.query(models.Game).filter(models.Game.id == character.game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")

    db_character = models.Character(**character.model_dump())
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character


@router.put("/{character_id}", response_model=schemas.CharacterResponse)
def update_character(
    character_id: int,
    character_update: schemas.CharacterCreate,
    x_admin_token: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """更新角色（管理员专用）"""
    if not x_admin_token or not verify_admin_token(x_admin_token):
        raise HTTPException(status_code=403, detail="需要管理员权限")

    db_character = db.query(models.Character).filter(models.Character.id == character_id).first()
    if not db_character:
        raise HTTPException(status_code=404, detail="角色不存在")

    # 如果更换了游戏，检查游戏是否存在
    if character_update.game_id != db_character.game_id:
        game = db.query(models.Game).filter(models.Game.id == character_update.game_id).first()
        if not game:
            raise HTTPException(status_code=404, detail="游戏不存在")

    for key, value in character_update.model_dump().items():
        setattr(db_character, key, value)

    db.commit()
    db.refresh(db_character)
    return db_character


@router.delete("/{character_id}")
def delete_character(
    character_id: int,
    x_admin_token: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """删除角色（管理员专用）"""
    if not x_admin_token or not verify_admin_token(x_admin_token):
        raise HTTPException(status_code=403, detail="需要管理员权限")

    db_character = db.query(models.Character).filter(models.Character.id == character_id).first()
    if not db_character:
        raise HTTPException(status_code=404, detail="角色不存在")

    db.delete(db_character)
    db.commit()
    return {"message": "角色已删除"}
