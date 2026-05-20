# XEERP\-FASTAPI Enterprise\-level Inventory \&amp; Sales Micro\-Service System

![Docs](https://img.shields.io/badge/%E6%96%87%E6%A1%A3-%E5%9C%A8%E7%BA%BF-green.svg?logo=readthedocs&label=Docs)
![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-orange.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-blue.svg)
![Redis](https://img.shields.io/badge/Redis-7.0+-red.svg)
![Vue3](https://img.shields.io/badge/Vue-3.x-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

## Introduction

This project is an **enterprise\-level ERP micro\-service system** focusing on inventory, procurement and sales management\. It is designed for small and medium\-sized manufacturing and circulation enterprises, covering system authority management, commodity management, inventory control, production management, procurement, sales, data reports, approval workflows and other core business modules\.

Built with a full asynchronous tech stack including **FastAPI \+ SQLAlchemy \+ MySQL \+ Redis**, the system adopts a unified Gateway access entry\. It consists of 10 independent business micro\-services deployed by business domains, supporting horizontal scaling and private deployment\. The front\-end management system is developed based on secondary development of **Vue3 \+ Vite \+ Element Plus \(RuoYi\-Vue3\)**\.

## System Architecture

The system adopts a three\-tier micro\-service architecture: **Gateway \+ Business Micro\-Services \+ Shared Core**\.
High\-performance asynchronous interfaces are built based on FastAPI; SQLAlchemy 2\.x provides fully asynchronous ORM database operations; Redis is used for data cache preheating and session management\. The unified Gateway centrally handles JWT authentication, IP traffic limiting and route forwarding\.

This architecture features clear service boundaries, unified technology stack, high decoupling, and is convenient for team collaboration, iterative development and daily maintenance\.

## Core Technology Stack

- **Programming Language**: Python 3\.12\+

- **Web Framework**: FastAPI \+ Uvicorn \+ Gunicorn \(High\-performance asynchronous HTTP service\)

- **ORM Framework**: SQLAlchemy 2\.x \+ asyncmy \(Fully asynchronous ORM \&amp; declarative modeling\)

- **Database**: MySQL 8\.0\+ \(Primary persistent storage, supports master\-slave read\-write separation\)

- **Cache Middleware**: Redis 7\.0\+ \(Session management, dictionary \&amp; parameter cache, flow limiting, hot inventory data cache\)

- **Serialization**: orjson \(High\-performance JSON serializer replacing default built\-in library\)

- **Authentication**: JWT \(pyjwt \+ passlib/bcrypt\) for secure user identity verification

- **Configuration Management**: pydantic\-settings \+ python\-dotenv \(\.env configuration loading \&amp; type validation\)

- **Task Scheduling**: APScheduler \(AsyncIOScheduler \+ custom 6/7\-digit Cron expression\)

- **Rate Limiting**: slowapi \+ Redis \(Gateway\-side IP access frequency control\)

- **Front\-end Framework**: Vue3 \+ Vite \+ Element Plus \(Secondary development based on RuoYi\-Vue3\)

## Micro\-Service List

|Service Name|Port|Core Responsibility|
|---|---|---|
|gateway|8000|Unified Gateway: Route forwarding, JWT authentication, IP limiting, CORS cross\-domain, unified log collection|
|system|8001|System Authority Service: User/Role/Menu/Department/Post/Dictionary/System Parameter/Operation Log/Timed Task|
|product|8002|Commodity Center: Commodity info/Category/Brand/Unit of measurement management|
|stock|8003|Inventory Center: Warehouse management/Real\-time inventory/Inventory flow records|
|production|8004|Production Center: BOM management/Production plan/Material requisition/Stock\-in/Material return/Loss statistics|
|report|8005|Report Center: Production progress/Material requisition details/Warehousing cost/Inventory account statement|
|approval|8006|Approval Workflow: Process definition/Approval node/Approval instance/Approval record|
|partner|8007|Business Partner Management: Unified management of customers and suppliers|
|order|8008|Order Center: Sales order \&amp; Purchase order management|
|purchase|8009|Procurement Center: Purchase order/Purchase receiving \&amp; warehousing business|

## Project Layered Specification

All micro\-services follow unified layered directory standards:

- **Controller Layer**: `api/v1/\*\_controller\.py` — Parameter parsing, service calling, unified response encapsulation

- **Service Layer**: `service/\*\.py` — Business logic arrangement, transaction control, cross\-data\-layer collaboration

- **DAO Layer**: `dao/\*\.py` — SQLAlchemy query encapsulation and basic ORM operations

- **Model Layer**: `models/\*\.py` — ORM entity models inherited from Base

- **Schema Layer**: `schemas/\*\.py` — Pydantic request and response data models

- **Client Layer**: `clients/\*\.py` — Encapsulated cross\-service HTTP invocation based on httpx

- **Shared Utils**: Global `utils/` directory — Unified response tool, pagination tool, log component, file upload, password encryption and other general tools

## Installation Guide

### 1\. Environment Preparation

- Install Python 3\.12 or above and configure system environment variables

- Deploy MySQL 8\.0\+, create database named `xeapp`

- Deploy and start Redis 7\.0\+, ensure default port accessible normally

### 2\. Clone Project

```bash
git clone your-project-repository-link
cd XEERP-FASTAPI
```

### 3\. Install Dependencies

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 4\. Initialize Configuration File

Copy template configuration file and modify database link, Redis address, JWT secret key and other core parameters:

```bash
copy .env.example .env
```

### 5\. Start Services in Order \(Start Gateway Last\)

```bash
# Terminal 1: System Service
cd system && python run.py
# Terminal 2: Commodity Service
cd product && python run.py
# Terminal 3: Inventory Service
cd stock && python run.py
# Terminal 4: Production Service
cd production && python run.py
# Terminal 5: Gateway Service
cd gateway && python run.py
```

## Usage Instructions

1. **Service Access**
After startup, visit `http://localhost:8000/api/docs` to access unified gateway Swagger API documentation; each independent service can also be accessed via `http://localhost:\{port\}/api/docs`\.

2. **Login Authentication**
Call interface `POST /api/auth/login` to obtain JWT Token; carry request header `Authorization: Bearer \&lt;token\&gt;` to access protected business interfaces\.

3. **Business Operation**
Call all business interfaces through unified gateway to complete commodity maintenance, inventory inquiry, production plan arrangement, order processing, data statistics and other daily operations\.

4. **Timed Task Management**
Manage scheduled tasks online via interfaces under `/api/job/\*`, support Cron configuration, start/stop and immediate execution\.

5. **Permission \&amp; Security**
Adopt RBAC permission model \(User\-Role\-Menu\), support department\-level data permission filtering; JWT token realizes online session management and forced offline function\.

6. **Front\-end Management System Startup**

```bash
cd web-ui
yarn install
yarn dev
# Access address: http://localhost:80
```

## Document Index

|No\.|Document Name|Main Content|
|---|---|---|
|01|\[Project Overview\]\(\./docs/01\-Project\-Overview\.md\)|Project positioning, functional layout, tech stack, service list|
|02|\[Quick Start\]\(\./docs/02\-Quick\-Start\.md\)|Environment deployment, installation steps, service startup \&amp; first interface call|
|03|\[System Architecture\]\(\./docs/03\-System\-Architecture\.md\)|Micro\-service architecture, request link, unified directory structure \&amp; layer responsibilities|
|04|\[Gateway \&amp; Routing\]\(\./docs/04\-Gateway\-Routing\.md\)|Gateway forwarding rule, JWT authentication, flow limiting \&amp; log mechanism|
|05|\[Auth \&amp; Permission\]\(\./docs/05\-Auth\-Permission\.md\)|Login process, RBAC design, password policy \&amp; online session control|
|06|\[Database \&amp; Cache\]\(\./docs/06\-DB\-Cache\.md\)|SQLAlchemy usage, Redis application, database naming specification \&amp; transaction management|
|07|\[Middleware \&amp; Exception Handling\]\(\./docs/07\-Middleware\-Exception\.md\)|CORS, GZip compression, link tracing \&amp; global exception handler|
|08|\[Common Utility Library\]\(\./docs/08\-Common\-Utils\.md\)|Unified response tool, pagination tool, log, file upload, password tool|
|09|\[Business Service Details\]\(\./docs/09\-Business\-Service\-Details\.md\)|Core logic of commodity, inventory, production, report, approval, order and procurement module|
|10|\[API Specification \&amp; Response Standard\]\(\./docs/10\-API\-Specification\.md\)|Unified response structure, status code definition, pagination rule \&amp; HTTP convention|
|11|\[Scheduled Task\]\(\./docs/11\-Scheduled\-Task\.md\)|APScheduler usage, Cron expression, task storage \&amp; execution log|
|12|\[Development Guide\]\(\./docs/12\-Development\-Guide\.md\)|New interface development, new service access, code specification \&amp; project deployment|
|13|\[Log System\]\(\./docs/13\-Log\-System\.md\)|Standard unified log system design and usage|

## Recommended Reading Sequence

- **Newcomer Access**: 01 Project Overview → 02 Quick Start → 03 System Architecture

- **In\-depth Study on Request Link \&amp; Gateway Mechanism**: 04 Gateway \&amp; Routing \+ 05 Auth \&amp; Permission

- **Business Secondary Development**: 09 Business Service Details \+ 12 Development Guide

- **Front\-end Interface Joint Debugging**: 10 API Specification \&amp; Response Standard

- **Operation \&amp; Maintenance Deployment \&amp; Online Release**: 02 Quick Start \+ Chapter 7 of Development Guide

## Project Directory Structure

```Plain Text
XEERP-FASTAPI/
├── gateway/          # Gateway Service (Route Forwarding, Auth, Rate Limit)
├── system/           # System Authority Service
├── product/          # Commodity Business Service
├── stock/            # Inventory Business Service
├── production/       # Production Business Service
├── report/           # Data Report Service
├── approval/         # Approval Workflow Service
├── partner/          # Customer & Supplier Management Service
├── order/            # Order Management Service
├── purchase/         # Procurement Business Service
├── utils/            # Global Shared Tool Library
├── web-ui/           # Vue3 Front-end Management System
├── docs/             # Complete Technical Documentation
├── .env.example      # Environment Configuration Template
└── requirements.txt  # Python Dependency List
```

## Contribution Guidelines

1. Fork this repository

2. Create your feature branch \(Feat\_xxx\)

3. Commit your changes

4. Submit Pull Request for code review

## Extended Features

1. Support multi\-language README documents via naming rule like `Readme\_en\.md`

2. Compatible with mainstream open source community specification standards

3. Complete open source project operation document system

4. Standard open source contribution specification \&amp; community operation guide
