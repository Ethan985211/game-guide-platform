from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .database import engine, Base
from .routers import auth, games, characters, articles, search, admin, openclaw, analytics

# 加载环境变量
load_dotenv()

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="游戏攻略聚合平台 API",
    description="多款游戏聚合的游戏攻略网站后端 API",
    version="1.0.0",
    root_path="/api"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
