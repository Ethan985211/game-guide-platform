# 邮件服务配置指南

## 概述

本项目已集成邮件发送功能，支持：
- 📧 邮箱验证（新用户注册后验证邮箱）
- 🔑 密码重置（忘记密码时发送重置链接）
- 🎉 欢迎邮件（验证成功后发送欢迎邮件）

## QQ邮箱配置

### 步骤1：获取QQ邮箱授权码

1. 登录QQ邮箱：https://mail.qq.com
2. 点击右上角 **设置** → **账户**
3. 向下滚动找到 **POP3/IMAP/SMTP/Exchange/CardDAV/CardDAV 服务**
4. 确保以下服务已开启：
   - **SMTP 服务** - 必须开启
5. 点击 **生成授权码**
6. 按提示发送短信验证
7. 获取16位授权码（格式：`xxxx xxxx xxxx xxxx`）

### 步骤2：配置环境变量

创建 `backend/.env` 文件（复制 `.env.example`）：

```env
EMAIL_USER=bodahaowu@qq.com
EMAIL_PASSWORD=你的授权码
EMAIL_FROM_NAME=游戏攻略平台
SITE_URL=http://localhost:5173
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**重要**：
- `EMAIL_USER` 填写您的QQ邮箱地址
- `EMAIL_PASSWORD` 填写刚刚获取的**授权码**（不是QQ密码！）
- `SITE_URL` 生产环境请改为实际域名

### 步骤3：安装依赖

```bash
cd backend
pip install -r requirements.txt
```

## 使用方法

### 后端API

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/auth/send-verification-email` | POST | 发送验证邮件 |
| `/api/auth/verify-email` | POST | 验证邮箱 |
| `/api/auth/forgot-password` | POST | 发送密码重置邮件 |
| `/api/auth/reset-password` | POST | 重置密码 |

### 前端页面

| 页面 | 路由 | 描述 |
|------|------|------|
| 登录页 | `/login` | 添加了"忘记密码"链接 |
| 注册页 | `/register` | 注册后自动发送验证邮件 |
| 验证页 | `/verify-email` | 邮箱验证结果页 |
| 重置页 | `/reset-password` | 密码重置页 |
| 个人中心 | `/profile` | 显示验证状态，可重新发送验证邮件 |

## 测试

### 本地测试

1. 启动后端服务：
```bash
cd backend
uvicorn app.main:app --reload
```

2. 使用curl测试发送邮件：
```bash
curl -X POST http://localhost:8000/api/auth/send-verification-email \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

## 常见问题

### Q: 发送邮件失败？

1. 检查授权码是否正确
2. 确保QQ邮箱的SMTP服务已开启
3. 检查防火墙是否阻止了SMTP端口（465或587）

### Q: 收不到邮件？

1. 检查垃圾邮件箱
2. 确保邮箱地址填写正确
3. 部分邮箱服务商可能会拦截

### Q: 授权码无效？

授权码有效期为长期，但同一授权码只能绑定一个客户端。如果在其他地方使用过，请重新生成。

## 安全建议

1. **不要泄露授权码**：授权码相当于第三方客户端的密码
2. **使用.env文件**：不要将授权码提交到版本控制系统
3. **定期更换**：建议定期更换授权码
4. **生产环境**：使用专用的企业邮箱或邮件服务（如SendGrid、Mailgun）

## 其他邮箱服务

如果想使用其他邮箱服务（如Gmail、企业邮箱），只需修改 `email_service.py` 中的配置：

```python
EMAIL_HOST = "smtp.gmail.com"  # Gmail SMTP服务器
EMAIL_PORT = 587  # Gmail使用587端口
```
