"""
邮件服务模块
支持QQ邮箱发送验证邮件、密码重置等功能
"""
import yagmail
import os
import hashlib
import time
from typing import Optional

# 邮件配置
EMAIL_HOST = "smtp.qq.com"
EMAIL_PORT = 465
EMAIL_USER = os.getenv("EMAIL_USER", "your-email@qq.com")  # 发件人邮箱
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")  # 授权码
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "游戏攻略平台")

# 网站配置
SITE_URL = os.getenv("SITE_URL", "http://localhost:5173")  # 前端地址

# Token有效期（秒）
EMAIL_VERIFY_TOKEN_EXPIRE = 3600  # 1小时
PASSWORD_RESET_TOKEN_EXPIRE = 1800  # 30分钟


class EmailService:
    """邮件服务类"""
    
    def __init__(self):
        self.host = EMAIL_HOST
        self.port = EMAIL_PORT
        self.user = EMAIL_USER
        self.password = EMAIL_PASSWORD
        self.from_name = EMAIL_FROM_NAME
    
    def _is_configured(self) -> bool:
        """检查邮件服务是否已配置"""
        return bool(self.user and self.password)
    
    def _generate_token(self, email: str, action: str, expire: int) -> str:
        """生成验证token"""
        data = f"{email}:{action}:{int(time.time())}:{expire}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _generate_verification_code(self, length: int = 6) -> str:
        """生成随机验证码"""
        import random
        return ''.join(random.choices('0123456789', k=length))
    
    async def send_email(self, to: str, subject: str, html_content: str) -> bool:
        """
        发送邮件
        
        Args:
            to: 收件人邮箱
            subject: 邮件主题
            html_content: HTML内容
        
        Returns:
            bool: 发送是否成功
        """
        if not self._is_configured():
            print(f"[警告] 邮件服务未配置，无法发送邮件到 {to}")
            print(f"[提示] 请设置环境变量 EMAIL_USER 和 EMAIL_PASSWORD")
            return False
        
        try:
            yag = yagmail.SMTP(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            yag.send(
                to=to,
                subject=subject,
                contents=html_content
            )
            print(f"[成功] 邮件已发送到 {to}")
            return True
        except Exception as e:
            print(f"[错误] 发送邮件失败: {str(e)}")
            return False
    
    async def send_verification_email(self, email: str, username: str, user_id: int) -> dict:
        """
        发送邮箱验证邮件
        
        Args:
            email: 用户邮箱
            username: 用户名
            user_id: 用户ID
        
        Returns:
            dict: 包含token和验证码的信息
        """
        # 生成token和验证码
        token = self._generate_token(email, "verify", EMAIL_VERIFY_TOKEN_EXPIRE)
        code = self._generate_verification_code()
        
        verify_url = f"{SITE_URL}/verify-email?token={token}&code={code}&user_id={user_id}"
        
        subject = f"【{self.from_name}】验证您的邮箱"
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0;">🎮 {self.from_name}</h1>
            </div>
            <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333;">您好，{username}！</h2>
                <p style="color: #666; line-height: 1.6;">
                    感谢您注册 {self.from_name}，请验证您的邮箱地址以完成注册。
                </p>
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center;">
                    <p style="color: #888; margin: 0 0 10px;">您的验证码：</p>
                    <span style="font-size: 32px; font-weight: bold; color: #667eea; letter-spacing: 8px;">{code}</span>
                </div>
                <p style="color: #888; font-size: 14px;">
                    或者点击以下链接验证：<br>
                    <a href="{verify_url}" style="color: #667eea;">{verify_url}</a>
                </p>
                <p style="color: #999; font-size: 12px; margin-top: 30px;">
                    ⚠️ 此验证码有效期为 1 小时，请勿将验证码告诉他人。<br>
                    如果您没有注册账号，请忽略此邮件。
                </p>
            </div>
        </div>
        """
        
        success = await self.send_email(email, subject, html_content)
        return {"success": success, "token": token, "code": code}
    
    async def send_password_reset_email(self, email: str, username: str, user_id: int) -> dict:
        """
        发送密码重置邮件
        
        Args:
            email: 用户邮箱
            username: 用户名
            user_id: 用户ID
        
        Returns:
            dict: 包含token的信息
        """
        token = self._generate_token(email, "reset", PASSWORD_RESET_TOKEN_EXPIRE)
        reset_url = f"{SITE_URL}/reset-password?token={token}&user_id={user_id}"
        
        subject = f"【{self.from_name}】密码重置请求"
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0;">🎮 {self.from_name}</h1>
            </div>
            <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333;">您好，{username}！</h2>
                <p style="color: #666; line-height: 1.6;">
                    我们收到了您的密码重置请求。如果您没有发起请求，请忽略此邮件。
                </p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_url}" style="display: inline-block; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 15px 40px; text-decoration: none; border-radius: 25px; font-weight: bold;">
                        重置密码
                    </a>
                </div>
                <p style="color: #888; font-size: 14px;">
                    或者复制链接到浏览器打开：<br>
                    <a href="{reset_url}" style="color: #f5576c; word-break: break-all;">{reset_url}</a>
                </p>
                <p style="color: #999; font-size: 12px; margin-top: 30px;">
                    ⚠️ 此链接有效期为 30 分钟，请尽快重置密码。<br>
                    如果您没有请求重置密码，您的账号可能被盗，请及时修改密码。
                </p>
            </div>
        </div>
        """
        
        success = await self.send_email(email, subject, html_content)
        return {"success": success, "token": token}
    
    async def send_welcome_email(self, email: str, username: str) -> bool:
        """
        发送欢迎邮件
        
        Args:
            email: 用户邮箱
            username: 用户名
        
        Returns:
            bool: 发送是否成功
        """
        subject = f"🎉 欢迎加入{self.from_name}！"
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0;">🎮 {self.from_name}</h1>
            </div>
            <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333;">欢迎，{username}！🎉</h2>
                <p style="color: #666; line-height: 1.6;">
                    感谢您完成邮箱验证！您现在可以：
                </p>
                <ul style="color: #666; line-height: 2;">
                    <li>浏览和搜索游戏攻略</li>
                    <li>发布您的游戏心得</li>
                    <li>与其他玩家交流互动</li>
                    <li>收藏喜欢的攻略文章</li>
                </ul>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{SITE_URL}" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 40px; text-decoration: none; border-radius: 25px; font-weight: bold;">
                        开始探索
                    </a>
                </div>
                <p style="color: #999; font-size: 12px;">
                    祝您游戏愉快！
                </p>
            </div>
        </div>
        """
        
        return await self.send_email(email, subject, html_content)


# 全局邮件服务实例
email_service = EmailService()
