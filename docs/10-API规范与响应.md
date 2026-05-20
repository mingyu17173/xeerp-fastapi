# 10 · API 规范与响应

---

## 一、统一响应格式

所有接口（包括异常）统一使用如下 JSON 结构：

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": { ... },
  "rows": [ ... ],
  "success": true,
  "time": "2026-05-15T10:00:00"
}
```

### 1.1 字段说明

| 字段 | 类型 | 含义 |
| ---- | ---- | ---- |
| `code` | int | 业务状态码，详见 §三 |
| `msg` | str | 人类可读提示 |
| `data` | any | 单条数据 |
| `rows` | list | 列表数据 |
| `success` | bool | 是否成功 |
| `time` | datetime | 服务器响应时间 |
| `total` | int | 仅分页：总记录数 |
| `pageNum` | int | 仅分页：当前页码 |
| `pageSize` | int | 仅分页：每页数量 |
| `hasNext` | bool | 仅分页：是否有下一页 |

### 1.2 分页列表响应

```json
{
  "code": 200,
  "msg": "操作成功",
  "rows": [...],
  "total": 100,
  "pageNum": 1,
  "pageSize": 10,
  "hasNext": true,
  "success": true,
  "time": "..."
}
```

---

## 二、HTTP 方法约定

| 操作 | 方法 | URL 示例 |
| ---- | ---- | -------- |
| 列表 | GET | `/api/product/list?pageNum=1&pageSize=10` |
| 详情 | GET | `/api/product/{id}` |
| 新增 | POST | `/api/product` |
| 修改 | PUT | `/api/product` |
| 删除 | DELETE | `/api/product/{id}` 或 `/api/product/{ids}` |
| 导出 | POST | `/api/product/export` |
| 导入 | POST | `/api/product/import` |

> 分页参数统一使用 `pageNum`（页码，从 1 开始）+ `pageSize`（每页数量）。

---

## 三、状态码定义

| code | 含义 | 触发条件 |
| ---- | ---- | -------- |
| `200` | 成功 | `ResponseUtil.success()` |
| `-1` | 业务失败（可预期） | `ResponseUtil.failure()` |
| `401` | 未认证 | Token 过期/无效 |
| `403` | 无权限 | 权限校验失败 |
| `500` | 系统异常 | 未处理异常 |

> **HTTP Status Code 始终为 200**（业务异常不使用 HTTP 4xx/5xx），前端以 `code` 字段为准。
> 例外：`HTTPException` 被框架原生处理时使用 HTTP 状态码。

---

## 四、请求体规范

- Content-Type：`application/json`（业务接口）或 `multipart/form-data`（文件上传）
- 字段命名：**camelCase**（前端侧），后端自动通过 `CamelCaseUtil.transform_result` 转换
- 空字段：不传即可，后端设默认值；传 `null` 等效

---

## 五、公共请求头

| Header | 说明 |
| ------ | ---- |
| `Authorization` | `Bearer {token}` |
| `Content-Type` | `application/json` |
| `X-Trace-Id` | 可选，链路追踪 ID（网关 / 前端传入） |

---

## 六、接口文档

每个微服务均暴露 FastAPI 自动生成的 Swagger/ReDoc：

| 服务 | Swagger | ReDoc |
| ---- | ------- | ----- |
| gateway | `http://localhost:8000/api/docs` | `/api/redoc` |
| system | `http://localhost:8001/api/docs` | `/api/redoc` |
| product | `http://localhost:8002/api/docs` | `/api/redoc` |
| 其他 | `http://localhost:{port}/api/docs` | ... |

---

## 七、错误响应示例

### 7.1 登录失败

```json
{ "code": -1, "msg": "用户名或密码错误", "success": false, "time": "..." }
```

### 7.2 Token 过期

```json
{ "code": 401, "msg": "登录信息已过期，访问系统资源失败", "success": false, "time": "..." }
```

### 7.3 服务异常

```json
{ "code": 500, "msg": "库存不足", "success": false, "time": "..." }
```
