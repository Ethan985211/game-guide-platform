from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import auth, games, characters, articles, comments, search

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="游戏攻略聚合平台 API",
    description="多款游戏聚合的游戏攻略网站后端 API",
    version="1.0.0",
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
app.include_router(comments.router)
app.include_router(search.router)


@app.get("/")
def root():
    return {"message": "游戏攻略聚合平台 API", "docs": "/docs"}


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
