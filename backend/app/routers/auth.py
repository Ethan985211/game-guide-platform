from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..database import get_db
from .. import models, schemas
from ..auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 检查邮箱是否存在
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="邮箱已被注册")

    # 检查用户名是否存在
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已被使用")

    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=schemas.UserResponse)
def update_me(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user_update.username:
        existing = db.query(models.User).filter(
            models.User.username == user_update.username,
            models.User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="用户名已被使用")
        current_user.username = user_update.username

    if user_update.bio is not None:
        current_user.bio = user_update.bio
    if user_update.avatar:
        current_user.avatar = user_update.avatar

    db.commit()
    db.refresh(current_user)
    return current_user
