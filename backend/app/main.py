import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, FileResponse
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv

from .database import engine, Base
from .middleware import RateLimitMiddleware, RequestLogMiddleware
from .routers import auth, games, characters, articles, search, admin, openclaw, analytics

load_dotenv()

# 启用 SQLite WAL 模式 + 优化
if "sqlite" in str(engine.url):
    with engine.connect() as conn:
        conn.execute(__import__("sqlalchemy").text("PRAGMA journal_mode=WAL"))
        conn.execute(__import__("sqlalchemy").text("PRAGMA synchronous=NORMAL"))
        conn.execute(__import__("sqlalchemy").text("PRAGMA cache_size=-8000"))  # 8MB cache
        conn.execute(__import__("sqlalchemy").text("PRAGMA busy_timeout=5000"))
        conn.commit()
    print("[数据库] SQLite WAL 模式已启用")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="游戏攻略聚合平台",
    description="多款游戏聚合的游戏攻略网站",
    version="2.0.0",
    root_path="/api",
    docs_url="/docs" if os.getenv("DISABLE_DOCS") != "true" else None,
    redoc_url=None,
)

# ---- 中间件链 ----
# 1. CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://82.156.34.78").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Gzip 压缩（大于 500 字节的响应自动压缩）
app.add_middleware(GZipMiddleware, minimum_size=500)

# 3. 速率限制（每 IP 每分钟 120 次请求）
app.add_middleware(RateLimitMiddleware, requests_per_minute=120)

# 4. 请求日志
app.add_middleware(RequestLogMiddleware)


# ---- 全局异常处理 ----
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"[ERROR] {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误"}
    )


# ---- 注册路由 ----
app.include_router(auth.router)
app.include_router(games.router)
app.include_router(characters.router)
app.include_router(articles.router)
app.include_router(search.router)
app.include_router(admin.router)
app.include_router(openclaw.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {
        "name": "游戏攻略聚合平台",
        "version": "2.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "db": "sqlite"}


# ---- 静态文件（头像等） ----
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(STATIC_DIR):
    from fastapi.staticfiles import StaticFiles
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
