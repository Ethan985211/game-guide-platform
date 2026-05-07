# Game Guide Platform - 游戏攻略聚合平台

多款游戏聚合的游戏攻略网站，支持文章发布、游戏数据库查询、用户社区互动。

## 功能特性

- 📰 **文章系统**: 游戏攻略、新闻发布与浏览
- 🎮 **游戏数据库**: 游戏信息、角色/武器数据库查询
- 💬 **社区互动**: 评论、点赞、用户中心
- 🔍 **全文搜索**: 快速查找游戏、文章、角色

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

### 后端启动

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 前端启动

```bash
cd frontend
npm install
npm run dev
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
│   │   └── routers/         # API 路由
│   └── requirements.txt
├── frontend/
│   └── src/
└── README.md
```

## License

MIT
