from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os

from .database import get_db
from . import models, schemas

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    # 确保 sub 是字符串
    if 'sub' in to_encode:
        to_encode['sub'] = str(to_encode['sub'])
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)  # 转换回整数
    except (JWTError, ValueError):
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: models.User = Depends(get_current_user)) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# ============ Admin Authentication ============

_admin_token_cache = {}


def authenticate_admin(username: str, password: str, db: Session = None) -> bool:
    """验证管理员账号密码（从数据库验证）"""
    from .models import AdminUser
    
    if db is None:
        from .database import SessionLocal
        db = SessionLocal()
        try:
            return _authenticate_admin_db(username, password, db)
        finally:
            db.close()
    return _authenticate_admin_db(username, password, db)


def _authenticate_admin_db(username: str, password: str, db: Session) -> bool:
    """从数据库验证管理员"""
    from .models import AdminUser
    admin = db.query(AdminUser).filter(AdminUser.username == username).first()
    if not admin:
        return False
    return verify_password(password, admin.password_hash)


def create_admin_in_db(username: str, password: str, db: Session = None):
    """在数据库中创建管理员"""
    from .models import AdminUser
    
    if db is None:
        from .database import SessionLocal
        db = SessionLocal()
        created = False
        try:
            created = _create_admin_in_db(username, password, db)
        finally:
            db.close()
        return created
    return _create_admin_in_db(username, password, db)


def _create_admin_in_db(username: str, password: str, db: Session) -> bool:
    """在数据库中创建管理员"""
    from .models import AdminUser
    
    existing = db.query(AdminUser).filter(AdminUser.username == username).first()
    if existing:
        return False
    
    admin = AdminUser(
        username=username,
        password_hash=get_password_hash(password)
    )
    db.add(admin)
    db.commit()
    return True


def create_admin_token() -> str:
    """创建管理员专用token"""
    import hashlib
    import time
    import secrets
    token_data = f"{secrets.token_hex(16)}:{int(time.time())}"
    token = hashlib.sha256(token_data.encode()).hexdigest()
    _admin_token_cache[token] = time.time()
    return token


def verify_admin_token(token: str) -> bool:
    """验证管理员token"""
    import time
    if token not in _admin_token_cache:
        return False
    # Token 有效期 24 小时
    if time.time() - _admin_token_cache[token] > 86400:
        del _admin_token_cache[token]
        return False
    return True


def get_current_admin_user(
    token: str = Depends(lambda: None),  # 占位，会被Depends覆盖
    db: Session = Depends(get_db)
) -> models.User:
    """获取当前管理员用户（如果已登录）"""
    pass  # 占位，由Depends提供实现


def require_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    """要求管理员权限的依赖"""
    user = get_current_user(token, db)
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return user


# ============ OpenClaw API Key Authentication ============

OPENCLAW_API_KEY = os.getenv("OPENCLAW_API_KEY", "")
OPENCLAW_API_SECRET = os.getenv("OPENCLAW_API_SECRET", "")


def verify_openclaw_api_key(api_key: str) -> bool:
    """验证OpenClaw API密钥"""
    if not OPENCLAW_API_KEY:
        return False
    return api_key == OPENCLAW_API_KEY


def get_openclaw_user(db: Session = Depends(get_db)) -> Optional[models.User]:
    """获取OpenClaw专用系统用户（用于AI操作）"""
    openclaw_user = db.query(models.User).filter(
        models.User.email == "openclaw@system.local"
    ).first()

    # 如果不存在，创建一个
    if not openclaw_user:
        openclaw_user = models.User(
            username="OpenClaw Agent",
            email="openclaw@system.local",
            hashed_password=get_password_hash("openclaw-system-only"),
            is_admin=True,
            is_active=True,
            is_verified=True,
            bio="AI智能体系统账号"
        )
        db.add(openclaw_user)
        db.commit()
        db.refresh(openclaw_user)

    return openclaw_user
