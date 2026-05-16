# Game Guide Platform - 游戏攻略聚合平台

多款游戏聚合的游戏攻略网站，支持文章发布、游戏数据库查询、用户社区互动。

## 功能特性

- 📰 **文章系统**: 游戏攻略、新闻发布与浏览
- 🎮 **游戏数据库**: 游戏信息、角色/武器数据库查询
- 💬 **社区互动**: 评论、点赞
- 🔍 **全文搜索**: 快速查找游戏、文章、角色
- 🔐 **管理员后台**: 用户管理、内容管理、数据统计
- 🤖 **OpenClaw智能体**: AI智能体API接入支持

## 技术栈

### 后端
- **框架**: FastAPI
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **ORM**: SQLAlchemy
- **认证**: JWT Token

### 前端
- **框架**: Vue 3 + Vite
- **状态管理**: Pinia
- **HTTP**: Axios
- **UI**: Element Plus

## 快速开始

### 一键启动（推荐）

```bash
# Windows
dev.bat

# macOS / Linux
chmod +x dev.sh && ./dev.sh
```

### 手动启动

```bash
# 后端启动
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 前端启动（新窗口）
cd frontend
npm install
npm run dev
```

## 管理员后台

访问 `http://localhost:5173/admin` 进入管理后台。

### 默认管理员账号

- **用户名**: `admin`
- **密码**: `admin123`

> ⚠️ 生产环境请务必修改 `.env` 中的管理员密码！

### 管理功能

- **仪表盘**: 平台数据统计
- **用户管理**: 用户列表、权限管理、账号禁用
- **游戏管理**: 添加、编辑、删除游戏
- **文章管理**: 审核、下架、删除文章

## OpenClaw 智能体 API

为AI智能体提供游戏攻略平台数据访问接口。

### API端点

| 功能 | 方法 | 端点 |
|------|------|------|
| 搜索游戏 | GET | `/api/openclaw/games/search?q={keyword}` |
| 游戏详情 | GET | `/api/openclaw/games/{id}` |
| 游戏角色 | GET | `/api/openclaw/games/{id}/characters` |
| 搜索文章 | GET | `/api/openclaw/articles/search?q={keyword}` |
| 文章详情 | GET | `/api/openclaw/articles/{id}` |
| 发表评论 | POST | `/api/openclaw/comments` |
| 平台统计 | GET | `/api/openclaw/stats` |
| AI查询 | POST | `/api/openclaw/query` |

### 认证方式

所有OpenClaw API请求需要在Header中包含API密钥：

```
X-API-Key: your-api-key
```

默认密钥: `openclaw_secret_key_2024`（可在后端 `.env` 中修改）

### 使用示例

```bash
# 搜索游戏
curl -X GET "http://localhost:8000/api/openclaw/games/search?q=原神" \
  -H "X-API-Key: openclaw_secret_key_2024"

# 获取平台统计
curl -X GET "http://localhost:8000/api/openclaw/stats" \
  -H "X-API-Key: openclaw_secret_key_2024"
```

## 环境变量配置

### 后端 (.env)

```env
# 数据库
DATABASE_URL=sqlite:///./game_guide.db

# 管理员配置
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# OpenClaw智能体
OPENCLAW_API_KEY=openclaw_secret_key_2024

# 邮件服务（可选）
EMAIL_USER=your-email@qq.com
EMAIL_PASSWORD=your-authorization-code
```

## API 文档

启动后端后访问: http://localhost:8000/docs

## 项目结构

```
├── backend/
│   ├── app/
│   │   ├── main.py          # 应用入口
│   │   ├── models.py        # 数据库模型
│   │   ├── schemas.py       # Pydantic 模型
│   │   ├── database.py      # 数据库配置
│   │   ├── auth.py         # 认证模块
│   │   └── routers/         # API 路由
│   │       ├── auth.py      # 用户认证
│   │       ├── admin.py     # 管理员API
│   │       └── openclaw.py  # 智能体API
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── pages/
│       │   └── admin/       # 管理后台页面
│       ├── stores/
│       │   └── admin.js     # 管理员状态
│       └── api/
└── README.md
```

## License

MIT
