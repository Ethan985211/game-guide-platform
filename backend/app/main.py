from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .database import engine, Base
from .routers import auth, games, characters, articles, search, admin, openclaw, analytics

# 加载环境变量
load_dotenv()

# 创建数据库表
Base.metadata.create_all(bind=engine)

import os

app = FastAPI(
    title="游戏攻略聚合平台 API",
    description="多款游戏聚合的游戏攻略网站后端 API",
    version="1.0.0",
    # nginx 反向代理：/api/* → backend，docs 从 /api/docs 访问
    root_path="/api",
)

# 配置 CORS（生产环境限制来源）
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://82.156.34.78").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(games.router)
app.include_router(characters.router)
app.include_router(articles.router)
# 评论功能已关闭
# app.include_router(comments.router)
app.include_router(search.router)
app.include_router(admin.router)
app.include_router(openclaw.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {
        "message": "游戏攻略聚合平台 API",
        "version": "1.0.0",
        "features": {
            "user_auth": "disabled",
            "admin_panel": "enabled",
            "openclaw_agent": "enabled"
        },
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
