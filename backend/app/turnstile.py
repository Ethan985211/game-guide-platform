"""
Cloudflare Turnstile 人机验证模块
"""
import httpx
import os
from typing import Optional


TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


async def verify_turnstile_token(token: str, ip: Optional[str] = None) -> bool:
    """
    验证 Cloudflare Turnstile token
    
    Args:
        token: Turnstile 生成的 token
        ip: 用户 IP 地址（可选）
    
    Returns:
        bool: 验证是否成功
    """
    # 获取 Secret Key
    secret_key = os.getenv("TURNSTILE_SECRET_KEY")
    
    # 如果没有配置 Secret Key
    if not secret_key:
        print("[Turnstile] 警告：未配置 TURNSTILE_SECRET_KEY，跳过人机验证")
        return True  # 开发模式跳过验证
    
    # 如果没有提供 token
    if not token:
        print("[Turnstile] 错误：未提供 token")
        return False
    
    # 调用 Turnstile API 验证
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                TURNSTILE_VERIFY_URL,
                data={
                    "secret": secret_key,
                    "response": token,
                    "remoteip": ip
                },
                timeout=10.0
            )
            
            result = response.json()
            
            if result.get("success"):
                print("[Turnstile] 验证成功")
                return True
            else:
                print(f"[Turnstile] 验证失败: {result.get('error-codes', [])}")
                return False
                
    except Exception as e:
        print(f"[Turnstile] 验证请求失败: {str(e)}")
        return False
