---
layout: post
title: "nanobot 新功能：定时任务与日历系统"
date: 2026-02-25 00:00:00 +0800
categories: AI开发
tags: [nanobot, AI助手, 定时任务, 日历, APScheduler, 开源项目]
author: Chris
read_time: 约6分钟
---

> 近期，nanobot-webui 迎来了重大更新，正式引入了**定时任务系统（Cron）**和**日历系统（Calendar）**。这两个功能的加入，让 nanobot 不再仅仅是一个对话助手，而是进化为一个真正的个人 AI 助手，能够帮你自动执行任务、管理日程。本文将详细介绍这两个新功能的使用方法和技术实现。

## 定时任务系统（Cron）

定时任务系统让 nanobot 能够按照预设的时间规则自动执行任务或发送提醒。

### 技术架构

nanobot 的 Cron 系统基于 **APScheduler** 构建，这是一个强大的 Python 定时任务库。整体架构如下：

| 组件 | 说明 |
|------|------|
| CronService | 核心调度服务，管理所有定时任务 |
| CronRepository | SQLite 持久化存储 |
| CronSkill | 对话中创建/管理任务的技能 |
| APScheduler | 底层任务调度引擎 |

### 三种触发模式

Cron 系统支持三种触发模式，满足不同场景需求：

#### 1. 一次性任务（at）

指定某个具体时间点执行一次，适合单次提醒：

```python
cron(action="add", message="下午3点开会", trigger_type="at", trigger_date_ms=1706256000000)
```

#### 2. 间隔任务（every）

按照固定间隔重复执行：

```python
# 每20分钟提醒一次
cron(action="add", message="Time to take a break!", every_seconds=1200)

# 每小时执行一次
cron(action="add", message="Check GitHub stars", every_seconds=3600)
```

#### 3. Cron 表达式（cron）

使用标准 Cron 表达式实现复杂的时间规则：

```python
# 每天早上8点
cron(action="add", message="早上好！", cron_expr="0 8 * * *")

# 工作日下午5点
cron(action="add", message="下班啦！", cron_expr="0 17 * * 1-5")

# 每周一早上9点例会
cron(action="add", message="周会时间到", cron_expr="0 9 * * 1")
```

### Cron 表达式对照表

| 用户表达 | 参数值 |
|---------|--------|
| every 20 minutes | `every_seconds: 1200` |
| every hour | `every_seconds: 3600` |
| every day at 8am | `cron_expr: "0 8 * * *"` |
| weekdays at 5pm | `cron_expr: "0 17 * * 1-5"` |

### 任务类型

每个定时任务可以配置两种执行方式：

1. **Reminder（提醒）** - 直接向用户发送消息
2. **Task（任务）** - 让 Agent 执行任务并返回结果

```python
# 提醒模式 - 直接发送消息
cron(action="add", message="Time to take a break!", every_seconds=1200)

# 任务模式 - Agent 执行任务
cron(action="add", message="Check GitHub stars and report", every_seconds=600)
```

### API 接口

Web UI 提供了完整的 REST API：

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/cron/jobs | 获取所有任务 |
| POST | /api/v1/cron/jobs | 创建新任务 |
| PATCH | /api/v1/cron/jobs/{id} | 更新任务 |
| DELETE | /api/v1/cron/jobs/{id} | 删除任务 |
| POST | /api/v1/cron/jobs/{id}/run | 手动执行任务 |

---

## 日历系统（Calendar）

日历系统为 nanobot 提供了完整的日程管理能力，基于 SQLite 本地存储，保护用户隐私。

### 数据模型

```python
class CalendarEvent:
    id: str              # 事件ID
    title: str           # 标题
    description: str     # 描述
    start_time: str      # 开始时间 (ISO格式)
    end_time: str        # 结束时间 (ISO格式)
    is_all_day: bool     # 是否全天事件
    priority: str        # 优先级 (low/medium/high)
    reminders: list      # 提醒列表
    recurrence: dict     # 重复规则
    recurrence_id: str   # 重复事件ID
```

### 功能特性

#### 事件管理
- 创建、读取、更新、删除日程事件
- 支持全天事件
- 支持事件优先级（低/中/高）
- 支持事件描述和备注

#### 重复事件
- 每日重复
- 每周重复
- 每月重复
- 自定义重复规则

#### 提醒设置
- 事件提醒通知
- 可配置提醒时间
- 支持声音提示

#### 个性化设置
- 默认视图：日视图、周视图、月视图
- 默认优先级
- 声音开关
- 通知开关

### API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/calendar/events | 获取事件列表 |
| POST | /api/v1/calendar/events | 创建事件 |
| PATCH | /api/v1/calendar/events/{id} | 更新事件 |
| DELETE | /api/v1/calendar/events/{id} | 删除事件 |
| GET | /api/v1/calendar/settings | 获取设置 |
| PATCH | /api/v1/calendar/settings | 更新设置 |

---

## 实际应用场景

### 场景一：定时提醒

> "每工作日下午5点提醒我提交日报"

```python
cron(action="add", message="该提交日报了！", cron_expr="0 17 * * 1-5")
```

### 场景二：定期任务执行

> "每小时检查一次 GitHub 仓库动态"

```python
cron(action="add", message="Check nanobot-webui GitHub stars", every_seconds=3600)
```

### 场景三：日程管理

通过 Web UI 或 API 创建和管理个人日程：

```json
POST /api/v1/calendar/events
{
  "title": "团队周会",
  "description": "每周一上午10点",
  "start_time": "2026-02-26T10:00:00",
  "end_time": "2026-02-26T11:00:00",
  "priority": "high",
  "is_all_day": false
}
```

### 场景四：智能提醒

结合记忆系统，AI 可以根据上下文智能提醒：

> "我记得你每周三要健身，记得穿运动服哦！"

---

## 技术亮点

### 1. 本地存储，数据安全

Cron 和 Calendar 数据都存储在本地 SQLite 数据库中（`~/.nanobot/cron.db` 和 `~/.nanobot/calendar.db`），不依赖第三方服务，保护用户隐私。

### 2. 异步架构，高效稳定

基于 `AsyncIOScheduler` 实现纯异步调度，配合 asyncio 事件循环，确保任务执行不会阻塞主服务。

### 3. 持久化设计

所有任务和日程都持久化到数据库，服务重启后自动恢复，无需担心数据丢失。

### 4. Web UI 集成

全新的 Web 管理界面让你可以可视化地管理定时任务和日历事件，无需编写代码。

---

## 未来规划

Cron 和 Calendar 功能还将持续优化：

- [ ] **与日历服务同步** - 支持 Google Calendar、Outlook 等第三方日历
- [ ] **智能日程建议** - AI 根据用户习惯推荐最佳会议时间
- [ ] **更丰富的提醒方式** - 邮件、短信、推送通知
- [ ] **自然语言创建任务** - "帮我设置每天早上8点的闹钟"

---

## 总结

定时任务和日历系统的加入，让 nanobot 从一个简单的对话助手，进化成为一个真正的**个人 AI 助手**。它不仅能回答问题，还能帮你自动执行任务、管理日程，成为你工作和生活中的得力助手。

如果你对这两个新功能感兴趣，欢迎访问 [nanobot-webui GitHub](https://github.com/codemo1991/nanobot-webui) 了解更多信息，也欢迎 Star 和贡献代码！

---

> **个人感受**：自从有了定时任务功能，我让 nanobot 每天早上自动给我发送天气提醒和日程汇总，真的大大提升了日常效率。加上日历系统，终于有一个可以跨平台同步的私有日程管理工具了！强烈推荐大家试试～