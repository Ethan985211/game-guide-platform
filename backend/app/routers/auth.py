from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
import random
import string
import os

from ..database import get_db
from .. import models, schemas
from ..auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
try:
    from ..email_service import email_service
except ImportError:
    email_service = None

router = APIRouter(prefix="/auth", tags=["认证"])


def generate_verification_code(length: int = 6) -> str:
    """生成随机验证码"""
    return ''.join(random.choices(string.digits, k=length))


@router.post("/send-verify-code", response_model=schemas.SendVerifyCodeResponse)
async def send_verify_code(request: schemas.SendVerifyCodeRequest, db: Session = Depends(get_db)):
    """发送邮箱验证码"""
    # 检查邮箱是否已注册
    db_user = db.query(models.User).filter(models.User.email == request.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="该邮箱尚未注册")

    # 生成验证码
    code = generate_verification_code()
    expires = datetime.now() + timedelta(minutes=5)

    # 保存验证码到数据库
    db_user.verification_code = code
    db_user.verification_expires = expires
    db.commit()

    # 发送邮件
    subject = "【游戏攻略平台】邮箱验证码"
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background: linear-gradient(135deg, #ff8c00 0%, #ff6b00 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="color: white; margin: 0;">游戏攻略平台</h1>
        </div>
        <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
            <h2 style="color: #333;">您好，{db_user.username}！</h2>
            <p style="color: #666; line-height: 1.6;">
                您收到了这封邮件是因为有人请求发送验证码。如果您没有请求，请忽略此邮件。
            </p>
            <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center;">
                <p style="color: #888; margin: 0 0 10px;">您的验证码：</p>
                <span style="font-size: 32px; font-weight: bold; color: #ff6b00; letter-spacing: 8px;">{code}</span>
            </div>
            <p style="color: #999; font-size: 12px; margin-top: 30px;">
                此验证码有效期为 5 分钟，请勿将验证码告诉他人。
            </p>
        </div>
    </div>
    """

    try:
        if email_service:
            await email_service.send_email(request.email, subject, html_content)
        else:
            print(f"[警告] 邮件服务不可用（yagmail未安装），验证码: {code}")
    except Exception as e:
        print(f"[警告] 邮件发送失败: {str(e)}")

    # 无论邮件发送成功与否，都返回成功（验证码已保存到数据库）
    return {"message": "验证码已发送", "expires_in": 300}


@router.post("/verify-code")
async def verify_code(request: schemas.VerifyCodeRequest, db: Session = Depends(get_db)):
    """验证邮箱验证码"""
    db_user = db.query(models.User).filter(models.User.email == request.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 检查验证码是否正确
    if db_user.verification_code != request.code:
        raise HTTPException(status_code=400, detail="验证码错误")

    # 检查验证码是否过期
    if db_user.verification_expires and datetime.now() > db_user.verification_expires:
        raise HTTPException(status_code=400, detail="验证码已过期")

    # 验证通过，更新用户状态
    db_user.is_verified = True
    db_user.verification_code = None
    db_user.verification_expires = None
    db.commit()

    return {"message": "验证成功"}


@router.post("/send-register-code", response_model=schemas.SendVerifyCodeResponse)
async def send_register_code(request: Request, req: schemas.SendRegisterCodeRequest, db: Session = Depends(get_db)):
    """发送注册验证码 - 已禁用"""
    raise HTTPException(status_code=403, detail="用户注册已禁用，请联系管理员")


@router.post("/register")
async def register(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
    """用户注册 - 已禁用"""
    raise HTTPException(status_code=403, detail="用户注册已禁用，请联系管理员")


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """用户登录 - 已禁用"""
    raise HTTPException(status_code=403, detail="用户登录已禁用，请使用管理员账号登录")


@router.post("/login-with-verify", response_model=schemas.Token)
async def login_with_verify(request: Request, login_data: schemas.LoginWithVerifyRequest, db: Session = Depends(get_db)):
    """带人机验证的登录接口 - 已禁用"""
    raise HTTPException(status_code=403, detail="用户登录已禁用，请使用管理员账号登录")


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


@router.post("/change-password", response_model=schemas.PasswordChangeResponse)
def change_password(
    request: schemas.PasswordChangeRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """修改密码"""
    from ..auth import verify_password, get_password_hash
    
    # 验证旧密码
    if not verify_password(request.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="原密码错误"
        )
    
    # 新密码长度检查
    if len(request.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="新密码长度不能少于6位"
        )
    
    # 更新密码
    current_user.hashed_password = get_password_hash(request.new_password)
    db.commit()
    
    return {"message": "密码修改成功"}


@router.post("/upload-avatar", response_model=schemas.AvatarUploadResponse)
async def upload_avatar(
    request: Request,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """上传头像（接收URL或base64）"""
    import os
    import base64
    import uuid
    from datetime import datetime
    
    try:
        body = await request.json()
        avatar_data = body.get("avatar")
        
        if not avatar_data:
            raise HTTPException(status_code=400, detail="请提供头像数据")
        
        # 如果是 base64 数据，保存为文件
        if avatar_data.startswith("data:image"):
            # 提取 base64 内容
            header, data = avatar_data.split(",", 1)
            image_data = base64.b64decode(data)
            
            # 确定文件扩展名
            ext = "png"
            if "jpeg" in header or "jpg" in header:
                ext = "jpg"
            elif "gif" in header:
                ext = "gif"
            elif "webp" in header:
                ext = "webp"
            
            # 生成文件名
            filename = f"{uuid.uuid4().hex}.{ext}"
            upload_dir = os.path.join(os.path.dirname(__file__), "..", "static", "avatars")
            os.makedirs(upload_dir, exist_ok=True)
            filepath = os.path.join(upload_dir, filename)
            
            # 保存文件
            with open(filepath, "wb") as f:
                f.write(image_data)
            
            # 生成访问URL
            avatar_url = f"/static/avatars/{filename}"
        else:
            # 直接使用URL
            avatar_url = avatar_data
        
        # 更新用户头像
        current_user.avatar = avatar_url
        db.commit()
        
        return {"message": "头像上传成功", "avatar_url": avatar_url}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"头像上传失败: {str(e)}")
