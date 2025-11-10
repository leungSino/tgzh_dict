# 🌍 tgzh_dict — 多语言翻译与学习平台

一个支持 **中文、塔吉克语、俄语、英语** 四种语言互译的在线平台，  
采用 **FastAPI + MongoDB + Vue 3 (Vite)** 架构构建。  
支持用户登录、词条录入与修改、操作记录与统计，  
未来将接入 AI 模型，实现智能翻译与语言学习功能。

---

## ✨ 项目功能

### ✅ 基础功能
- 多语言词条查询（中 / 塔 / 俄 / 英）
- 后台词条录入、修改、删除
- 不同角色权限管理（管理员 / 操作员 / 游客）
- 操作日志记录与查看（新增、修改、删除）
- 数据存储于 MongoDB

### 🚀 规划功能
- AI 翻译接口（GPT / NLLB / M2M 模型）
- 用户自定义词典
- 翻译历史与统计分析
- 多语言语音播放与输入支持

---

## 🏗️ 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 后端 | FastAPI | 高性能 Python Web 框架 |
| 数据库 | MongoDB | 文档型数据库，存储多语言词条与日志 |
| 前端 | Vue 3 + Vite | 现代化前端框架与构建工具 |
| 接口测试 | FastAPI Docs / Postman | RESTful API 接口调试 |
| 部署 | uvicorn / nginx | 本地开发与云端部署 |
| 版本控制 | Git + GitHub | 多分支开发与协作 |

---


## 📂 项目结构

```bash

tgzh_dict/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── utils.py
│   │   ├── models/
│   │   │   ├── user_model.py
│   │   │   └── translation_model.py
│   │   ├── services/
│   │   │   ├── user_service.py
│   │   │   ├── translation_service.py
│   │   │   └── log_service.py
│   │   └── routes/
│   │       ├── auth_routes.py
│   │       ├── translation_routes.py
│   │       └── log_routes.py
│   ├── requirements.txt
│   └── run.sh
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── assets/
│       │    └── style.css
│       ├── router/
│       │    └── index.js
│       ├── store/
│       │    └── userStore.js
│       ├── api/
│       │    └── api.js
│       ├── views/
│       │    ├── HomeView.vue
│       │    ├── LoginView.vue
│       │    └── AdminDashboard.vue
│       └── components/
│            ├── Navbar.vue
│            ├── WordForm.vue
│            ├── WordTable.vue
│            └── AdminLogs.vue
│
├── .gitignore
└── README.md
```

## 快速启动（后端）
```bash

cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export MONGO_URI="mongodb://localhost:27017"
export JWT_SECRET="change_this_secret"
uvicorn app.main:app --reload

## 前端
cd frontend
npm install
npm run dev
```
访问:
- 前端: http://localhost:5173
- 后端 docs: http://localhost:8000/docs
