# XEERP-FASTAPI 企业级进销存微服务系统

![Docs](https://img.shields.io/badge/%E6%96%87%E6%A1%A3-%E5%9C%A8%E7%BA%BF-green.svg?logo=readthedocs&label=Docs)
![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-orange.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-blue.svg)
![Redis](https://img.shields.io/badge/Redis-7.0+-red.svg)
![Vue3](https://img.shields.io/badge/Vue-3.x-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)


#### 介绍

🥇🥇🥇本项目为**企业级进销存（ERP）微服务系统**，面向中小制造与流通型企业，覆盖系统权限、商品、库存、生产、采购、销售、报表、审批等业务领域。采用 **FastAPI + SQLAlchemy + MySQL + Redis** 全异步技术栈构建，通过 **Gateway 网关统一接入**，10 个微服务按业务域独立部署，支持水平扩展与私有化部署需求。前端基于 **Vue3 + Vite + Element Plus**（RuoYi-Vue3 二次开发）提供管理后台。

#### 软件架构

本系统采用**网关 + 业务微服务 + 共享内核**的三段式微服务架构，基于 FastAPI 搭建高性能异步接口服务，使用 SQLAlchemy 2.x 全异步 ORM 操作数据库，Redis 提供缓存预热与会话管理，Gateway 网关统一处理 JWT 鉴权、IP 限流、路由转发。整体架构服务边界清晰、技术栈统一、解耦性强、便于多人协作与迭代维护。

#### 核心技术栈

- **开发语言**：Python 3\.12\+

- **Web 框架**：FastAPI + uvicorn + gunicorn（高性能异步 HTTP 服务）

- **ORM 框架**：SQLAlchemy 2\.x + asyncmy（全异步 ORM、声明式建模）

- **数据库**：MySQL 8\.0\+（主存储，支持主从读写分离）

- **缓存中间件**：Redis 7\.0\+（会话管理、字典/参数缓存、限流、库存热点）

- **序列化**：orjson（高性能 JSON 序列化替换默认 json）

- **鉴权机制**：JWT（pyjwt + passlib/bcrypt）实现用户身份安全校验

- **配置管理**：pydantic-settings + python-dotenv（.env 配置加载、类型校验）

- **定时调度**：APScheduler（AsyncIOScheduler + 自定义 6/7 位 Cron 表达式）

- **限流**：slowapi + Redis（网关侧 IP 速率限制）

- **前端**：Vue3 + Vite + Element Plus（基于 RuoYi-Vue3 二次开发）

#### 微服务清单

| 服务 | 端口 | 职责 |
| ---- | ---- | ---- |
| gateway | 8000 | 统一网关：路由转发、JWT 鉴权、IP 限流、CORS、日志 |
| system | 8001 | 系统权限：用户/角色/菜单/部门/岗位/字典/参数/日志/定时任务 |
| product | 8002 | 商品中心：商品/分类/品牌/计量单位 |
| stock | 8003 | 库存中心：仓库/实时库存/库存流水 |
| production | 8004 | 生产中心：BOM/生产计划/领料/入库/退料/损耗 |
| report | 8005 | 报表中心：生产进度/领料明细/入库成本/库存台账 |
| approval | 8006 | 审批流：流程定义/节点/审批实例/审批记录 |
| partner | 8007 | 往来单位：客户/供应商统一管理 |
| order | 8008 | 订单中心：销售订单/采购订单 |
| purchase | 8009 | 采购中心：采购单/采购收货入库 |

#### 项目分层结构

每个微服务遵循统一的分层目录约定：

- **Controller 层**：`api/v1/*_controller.py`，解析参数、调用 Service、返回 ResponseUtil 响应

- **Service 层**：`service/*.py`，业务编排、事务管理、跨 DAO 协同

- **DAO 层**：`dao/*.py`，SQLAlchemy 查询封装、ORM 操作

- **Model 层**：`models/*.py`，ORM 实体（继承 Base）

- **Schema 层**：`schemas/*.py`，请求/响应 pydantic 模型

- **Client 层**：`clients/*.py`，跨服务 HTTP 调用（httpx 封装）

- **共享工具库**：根目录 `utils/`，包含 ResponseUtil、PageUtil、日志、上传、密码等通用工具

#### 安装教程

本项目支持本地开发环境部署，操作简单、依赖轻量化，具体安装步骤如下：

1. **环境准备**
安装 **Python 3.12** 及以上版本，并配置好本地 Python 环境变量；
安装 **MySQL 8.0+** 数据库，创建 `xeapp` 数据库；
安装 **Redis 7.0+** 服务并启动，保证默认端口可正常访问。

2. **克隆项目仓库**
打开终端，执行以下命令拉取项目源码：
```bash
git clone 项目仓库地址
cd XEERP-FASTAPI
```

3.  **安装项目依赖**
使用 pip 批量安装所有依赖包：
```bash
python -m venv .venv
.\.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

4.  **初始化配置文件**
复制 `.env.example` 为 `.env`，修改数据库连接、Redis 地址、JWT 密钥等参数：
```bash
copy .env.example .env
```

5.  **启动项目服务**
按顺序启动各微服务（网关最后启动）：
```bash
cd system && python run.py       # 终端1: 系统服务 :8001
cd product && python run.py      # 终端2: 商品服务 :8002
cd stock && python run.py        # 终端3: 库存服务 :8003
cd production && python run.py   # 终端4: 生产服务 :8004
cd gateway && python run.py      # 终端5: 网关服务 :8000
```

#### 使用说明

1. **服务访问**
项目启动成功后，访问 `http://localhost:8000/api/docs` 查看网关 Swagger 接口文档，各服务也可独立访问 `http://localhost:{port}/api/docs`。

2. **登录认证**
调用 `POST /api/auth/login` 获取 JWT Token，后续请求携带 `Authorization: Bearer <token>` 访问受保护接口。

3. **业务操作**
通过统一网关调用各业务接口，完成商品管理、库存查询、生产计划、订单处理、报表查看等操作。

4. **定时任务管理**
通过 `/api/job/*` 接口在线管理定时任务，支持 Cron 表达式配置、启停、立即执行。

5. **权限与安全**
系统采用 RBAC 权限模型（用户-角色-菜单），支持数据权限（部门级别过滤），JWT 令牌支持在线会话管理与强制下线。

6. **前端管理后台**
```bash
cd web-ui
yarn install
yarn dev              # 开发模式 http://localhost:80
```


#### 📚 文档索引

| 序号 | 文档 | 内容主题 |
| ---- | ---- | -------- |
| 01 | [项目概览](./docs/01-项目概览.md) | 项目定位、功能版图、技术栈、服务清单 |
| 02 | [快速开始](./docs/02-快速开始.md) | 环境准备、安装、启动、第一次登录调用 |
| 03 | [系统架构](./docs/03-系统架构.md) | 微服务架构、请求链路、统一目录结构、分层职责 |
| 04 | [网关与路由](./docs/04-网关与路由.md) | Gateway 转发、JWT 鉴权、限流、日志 |
| 05 | [认证与权限](./docs/05-认证与权限.md) | 登录流程、RBAC、密码策略、在线会话 |
| 06 | [数据库与缓存](./docs/06-数据库与缓存.md) | SQLAlchemy、Redis、表命名、事务管理 |
| 07 | [中间件与异常](./docs/07-中间件与异常.md) | CORS、GZip、Trace、全局异常处理器 |
| 08 | [公共工具库](./docs/08-公共工具库.md) | ResponseUtil、PageUtil、日志、上传、密码 |
| 09 | [业务服务详解](./docs/09-业务服务详解.md) | 商品、库存、生产、报表、审批、订单、采购 |
| 10 | [API 规范与响应](./docs/10-API规范与响应.md) | 统一响应体、状态码、分页、HTTP 约定 |
| 11 | [定时任务](./docs/11-定时任务.md) | APScheduler、Cron 表达式、JobStore、执行日志 |
| 12 | [开发指南](./docs/12-开发指南.md) | 新增接口、新增服务、代码规范、部署 |
| 12 | [开发指南](./docs/13-日志系统.md) | 新增标准日志系统 |


#### 🗺️ 推荐阅读路线

- **新手入门 / 初次接入项目**：`01 项目概览` → `02 快速开始` → `03 系统架构`，快速建立整体认知

- **理解请求链路与网关机制**：重点研读 `04 网关与路由` + `05 认证与权限`

- **业务功能二次开发**：优先阅读 `09 业务服务详解` + `12 开发指南`

- **前端对接、接口联调**：直接查阅 `10 API 规范与响应`

- **运维部署、环境适配与上线**：参考 `02 快速开始` + `12 开发指南 §七`

#### 🧱 项目结构速览

```
XEERP-FASTAPI/
├── gateway/          网关服务（路由转发、JWT、限流）
├── system/           系统权限服务（用户、角色、菜单、定时任务）
├── product/          商品中心
├── stock/            库存中心
├── production/       生产中心
├── report/           报表中心
├── approval/         审批流
├── partner/          往来单位
├── order/            订单中心
├── purchase/         采购中心
├── utils/            共享工具库（ResponseUtil、PageUtil、日志等）
├── web-ui/           前端管理后台（Vue3 + Vite + Element Plus）
├── docs/             项目技术文档（12篇）
├── .env.example      配置模板
└── requirements.txt  Python 依赖
```

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat\_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
