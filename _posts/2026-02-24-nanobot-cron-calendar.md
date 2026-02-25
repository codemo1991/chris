---
layout: post
title: "nanobot 新功能：定时任务与日历系统"
date: 2026-02-24 00:00:00 +0800
categories: AI开发
tags: [nanobot, AI助手, 定时任务, 日历, APScheduler, 开源项目]
author: 技术博主
read_time: 约6分钟
description: nanobot新增定时任务和日历系统，让AI助手能够主动执行任务和管理时间。
---

> nanobot 近期又带来了两个重磅新功能：**定时任务（Cron）** 和 **日历系统（Calendar）**。这两个功能让 nanobot 不再只是一个被动的 AI 助手，而是能够主动为你执行任务、管理时间的智能助手。今天就让我们一起来详细了解一下这两个新功能。

## 为什么需要定时任务？

在日常工作和生活中，我们经常需要：

- 定时提醒自己做某件事情
- 定期执行一些自动化任务
- 定时获取某些信息（比如天气、股票等）

以前这些任务需要借助外部工具或者手动完成，现在 nanobot 可以帮你自动完成！

## 定时任务系统（Cron）

nanobot 的定时任务系统基于强大的 [APScheduler](https://apscheduler.readthedocs.io/) 库开发，支持多种触发方式：

### 支持的触发类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `at` | 一次性任务 | 今天下午3点提醒开会 |
| `every` | 间隔任务 | 每隔30分钟检查股票行情 |
| `cron` | 定时表达式 | 每天早上8点发送天气 |

### 定时表达式（Cron）示例

```bash
# 每天早上8点
cron(action="add", message="早上好，帮我查一下今天天气", cron_expr="0 8 * * *")

# 工作日下午5点提醒下班
cron(action="add", message="下班时间到！", cron_expr="0 17 * * 1-5")

# 每隔20分钟
cron(action="add", message="Time to take a break!", every_seconds=1200)
```

### 技术实现

定时任务系统采用 SQLite 数据库持久化存储，确保任务不会丢失：

```python
# 任务存储结构
{
    "id": "abc12345",
    "name": "天气提醒",
    "enabled": True,
    "trigger": {
        "type": "cron",
        "cronExpr": "0 8 * * *",
        "tz": "Asia/Shanghai"
    },
    "payload": {
        "kind": "agent_turn",
        "message": "帮我查一下今天深圳的天气"
    },
    "lastRunAtMs": 1706150400000,
    "nextRunAtMs": 1706236800000,
    "lastStatus": "ok"
}
```

### 核心功能特性

- ✅ **持久化存储** - 任务保存在 SQLite 数据库中，重启不丢失
- ✅ **多种触发方式** - 支持一次性、间隔、定时表达式
- ✅ **状态追踪** - 记录任务执行状态和错误信息
- ✅ **手动执行** - 支持强制运行某个任务
- ✅ **Web UI 管理** - 可在 Web 界面直观管理任务

## 日历系统（Calendar）

nanobot 还新增了完整的日历系统，让你可以在 AI 助手中管理日程安排！

### 功能特性

| 功能 | 说明 |
|------|------|
| 📅 事件管理 | 创建、编辑、删除日历事件 |
| 🔄 重复事件 | 支持每日、每周、每月重复 |
| ⚙️ 个性化设置 | 默认视图、优先级、通知偏好 |
| 💾 数据持久化 | SQLite 本地存储 |

### API 接口

```bash
# 获取事件
GET /api/v1/calendar/events?start_time=2026-02-24&end_time=2026-03-01

# 创建事件
POST /api/v1/calendar/events
{
    "title": "团队会议",
    "start_time": "2026-02-25T10:00:00",
    "end_time": "2026-02-25T11:00:00",
    "description": "周例会"
}

# 更新事件
PATCH /api/v1/calendar/events/{eventId}

# 删除事件
DELETE /api/v1/calendar/events/{eventId}
```

### 数据库设计

```sql
-- 事件表
CREATE TABLE calendar_events (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    start_time INTEGER NOT NULL,
    end_time INTEGER,
    all_day INTEGER DEFAULT 0,
    recurrence_id TEXT,
    recurrence_rule TEXT,
    reminder_minutes INTEGER,
    created_at INTEGER,
    updated_at INTEGER
);

-- 设置表
CREATE TABLE calendar_settings (
    id INTEGER PRIMARY KEY,
    default_view TEXT DEFAULT 'month',
    default_priority INTEGER DEFAULT 2,
    sound_enabled INTEGER DEFAULT 1,
    notification_enabled INTEGER DEFAULT 1
);
```

## 实际使用场景

### 场景一：定时天气提醒

```
用户：每天早上8点帮我查天气
nanobot：已设置定时任务「天气提醒」，每天早上8:00执行
```

### 场景二：会议日程管理

```
用户：帮我记录今天下午3点有个开发评审会议
nanobot：已创建日历事件「开发评审会议」，今天 15:00-16:00
```

### 场景三：定期数据收集

```
用户：每小时帮我查一下GitHub热门项目
nanobot：已设置间隔任务，每小时执行一次
```

## 技术亮点

### 1. 异步执行

定时任务采用 `AsyncIO` 异步执行，不会阻塞主线程：

```python
self._scheduler = AsyncIOScheduler(
    executors={"default": AsyncIOExecutor()},
    job_defaults={"coalesce": True, "max_instances": 1},
)
```

### 2. 智能同步

Web UI 创建的任务可以实时同步到调度器：

```python
async def sync_from_db(self) -> None:
    """将调度器与数据库中的任务同步"""
    # 移除已删除/已禁用的任务
    # 添加新启用的任务
```

### 3. 错误处理

完善的错误捕获和日志记录：

```python
except Exception as e:
    self.repository.update_job_status(
        job_id=job_id,
        last_run_at_ms=start_ms,
        last_status="error",
        last_error=str(e),
    )
```

## 未来展望

定时任务和日历系统只是开始，未来计划：

- 📧 **邮件通知** - 任务执行结果邮件通知
- 🔗 **第三方日历同步** - Google Calendar、Outlook 同步
- 📊 **任务统计** - 执行次数、成功率分析
- 🤖 **智能建议** - AI 推荐合适的提醒时间

## 总结

定时任务和日历系统的加入，让 nanobot 从一个「被动」的 AI 助手进化为「主动」的智能管家：

- ⏰ **定时任务** - 让你不再错过重要时刻
- 📅 **日历系统** - 帮你管理日程安排
- 🔄 **两者结合** - 实现更强大的自动化工作流

这两个功能的实现也展示了 nanobot 在系统架构上的成长——从单一的消息处理，到支持复杂的定时调度和数据持久化。

项目地址：[https://github.com/codemo1991/nanobot-webui](https://github.com/codemo1991/nanobot-webui)

---

> **使用建议**：赶紧试试设置几个定时任务吧！比如每天早上让 nanobot 给你发天气预报，或者设置一个每小时提醒自己喝水的小任务～ 🚀
