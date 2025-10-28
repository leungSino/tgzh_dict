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

## 🧩 项目结构

tgzh_dict/

│

├── backend/ # 后端目录 (FastAPI)

│ ├── main.py # 项目入口

│ ├── models/ # 数据模型定义

│ ├── routes/ # 路由 (API 接口)

│ ├── services/ # 服务逻辑

│ ├── database.py # MongoDB 连接

│ ├── auth/ # 用户登录与权限管理

│ └── utils/ # 工具与日志

│

├── frontend/ # 前端目录 (Vue 3)

│ ├── src/

│ │ ├── views/ # 页面 (登录、词典、统计等)

│ │ ├── components/ # 可复用组件

│ │ ├── store/ # Vuex / Pinia 状态管理

│ │ ├── router/ # 路由配置

│ │ ├── api/ # 前端请求封装

│ │ └── assets/ # 静态资源

│ └── vite.config.js

│

├── .gitignore

├── requirements.txt # Python 依赖

├── package.json # 前端依赖

├── README.md # 项目说明文件

└── LICENSE # 开源协议（MIT / Apache 2.0）
