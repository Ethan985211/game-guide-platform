"""
安全增强中间件 - 速率限制、请求日志、gzip 压缩
"""
import time
import json
from collections import defaultdict
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    """简易内存速率限制（单机模式，适合 SQLite 部署）"""
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.rate = requests_per_minute
        self.window = 60  # 秒
        self.clients: dict = defaultdict(list)
    
    def _get_client_id(self, request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"
    
    async def dispatch(self, request: Request, call_next):
        # 跳过健康检查和静态文件
        if request.url.path in ("/health", "/api/health", "/api/docs", "/api/openapi.json"):
            return await call_next(request)
        
        client_id = self._get_client_id(request)
        now = time.time()
        
        # 清理过期记录
        self.clients[client_id] = [
            t for t in self.clients[client_id] if now - t < self.window
        ]
        
        if len(self.clients[client_id]) >= self.rate:
            retry_after = int(self.window - (now - self.clients[client_id][0]))
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": "请求过于频繁，请稍后再试",
                    "retry_after": max(retry_after, 1)
                },
                headers={"Retry-After": str(max(retry_after, 1))}
            )
        
        self.clients[client_id].append(now)
        return await call_next(request)


class RequestLogMiddleware(BaseHTTPMiddleware):
    """请求日志中间件"""
    
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        
        # 只记录 API 请求
        if request.url.path.startswith("/api"):
            print(
                f"[{response.status_code}] {request.method} {request.url.path} "
                f"- {duration:.3f}s"
            )
        
        return response


def add_security_headers(request: Request, call_next):
    """移除安全敏感头"""
    response = call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers.pop("Server", None)
    response.headers.pop("X-Powered-By", None)
    return response
