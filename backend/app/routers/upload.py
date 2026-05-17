import os
import uuid
import imghdr
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user

router = APIRouter(prefix="/upload", tags=["图片上传"])

# 图片存储目录
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 允许的图片类型
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp", "image/bmp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def get_image_dimensions(filepath: str) -> tuple:
    """获取图片宽高，不依赖 PIL"""
    try:
        from PIL import Image
        with Image.open(filepath) as img:
            return img.size
    except ImportError:
        return None, None


@router.post("/image", response_model=schemas.ImageUploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """上传文章图片（需登录）"""
    # 校验文件类型
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"不支持的图片类型：{file.content_type}，仅支持 JPEG/PNG/GIF/WebP/BMP")

    # 读取文件内容
    content = await file.read()

    # 校验文件大小
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"图片大小不能超过 10MB，当前 {len(content) // 1024 // 1024}MB")

    # 二次校验：通过文件头确认真实类型
    import io
    real_type = imghdr.what(None, h=content[:32])
    if real_type is None:
        raise HTTPException(status_code=400, detail="无法识别的图片格式")
    if real_type == "jpeg":
        mime = "image/jpeg"
    elif real_type == "png":
        mime = "image/png"
    elif real_type == "gif":
        mime = "image/gif"
    elif real_type == "webp":
        mime = "image/webp"
    else:
        mime = f"image/{real_type}"

    # 生成唯一文件名
    ext = os.path.splitext(file.filename or "image.png")[1].lower()
    if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"):
        ext = ".png"
    unique_name = f"{uuid.uuid4().hex}{ext}"

    # 按日期分目录存储
    date_dir = datetime.now().strftime("%Y/%m")
    full_dir = os.path.join(UPLOAD_DIR, date_dir)
    os.makedirs(full_dir, exist_ok=True)

    filepath = os.path.join(full_dir, unique_name)
    with open(filepath, "wb") as f:
        f.write(content)

    # 获取图片尺寸
    width, height = get_image_dimensions(filepath)

    # 记录到数据库
    db_image = models.ArticleImage(
        filename=f"{date_dir}/{unique_name}",
        original_name=file.filename or "image.png",
        file_size=len(content),
        mime_type=mime,
        width=width,
        height=height,
        uploader_id=current_user.id,
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    # 返回可访问的 URL
    url = f"/static/uploads/{db_image.filename}"

    return schemas.ImageUploadResponse(
        id=db_image.id,
        url=url,
        filename=unique_name,
        original_name=db_image.original_name,
        file_size=db_image.file_size,
        mime_type=db_image.mime_type,
        width=db_image.width,
        height=db_image.height,
    )
