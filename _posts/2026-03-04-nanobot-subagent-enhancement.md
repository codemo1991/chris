---
title: "nanobot 重磅更新：子 Agent 能力全面增强"
date: 2026-03-04
tags: [nanobot, AI Agent, Claude Code, 子Agent, 性能优化]
description: "本次更新聚焦子 Agent 能力增强，带来 vision 模板去重、vision-exec 冲突检测、超时后台执行、Web UI SSE 重连等重磅功能"
---

# nanobot 重磅更新：子 Agent 能力全面增强

大家好！今天给大家带来 nanobot-webui 的重大版本更新。本次更新聚焦于**子 Agent 能力的全面增强**，涉及约 **1800+ 行代码变更**，涵盖了性能优化、用户体验提升、开发体验改善等多个维度。让我们一起来看看这次更新有哪些亮点吧！🎉

## 📌 更新概览

| 优化项 | 核心价值 |
|--------|----------|
| Vision 模板智能去重 | 减少重复调用，节省 token 消耗 |
| Vision-Exec 冲突检测 | 避免图片处理冲突，提升执行成功率 |
| 超时任务后台执行 | 用户无需等待，任务完成后自动通知 |
| Web UI SSE 重连 | 刷新页面也能继续接收推送 |
| 子 Agent 技能配置 | 支持为不同模板绑定特定技能 |
| 工具实例缓存 | 减少重复创建，提升响应速度 |

---

## 🧠 1. Vision 模板智能去重

### 问题背景

在之前的版本中，当用户发送多张图片或同一张图片时，系统可能会多次调用 vision 模板进行分析，造成不必要的 token 浪费和响应延迟。

### 解决方案

```python
# vision：本回合已有任一 vision spawn 即视为重复
if new_template == "vision":
    if any(
        s.get("name") == "spawn"
        and str((s.get("arguments") or {}).get("template", "")).lower() == "vision"
        for s in tool_steps
    ):
        return True  # 去重！
```

同时，针对 vision 模板使用了**更低的相似度阈值（0.55）**，相比默认的 0.78 更加严格，有效减少重复 spawn。

### 实际收益

- 🚀 **Token 节省**：避免同一图片的重复分析
- ⚡ **响应提速**：减少不必要的 API 调用
- 💰 **成本优化**：降低 token 消耗

---

## ⚔️ 2. Vision-Exec 冲突检测

### 问题背景

当用户同时发送图片并要求执行命令时，系统可能并行执行 `spawn(vision)` 和 `exec(图片相关命令)`，导致资源竞争或执行顺序不确定。

### 解决方案

新增 `_resolve_vision_exec_groups` 方法，自动检测并串行化这类冲突场景：

```python
def _resolve_vision_exec_groups(
    self,
    tool_calls: list,
    image_files: list[str],
) -> list[list] | None:
    # 检测 spawn(vision) + exec(图片相关) 冲突
    # 串行分组：vision 先行，再 exec
    # 多个 vision spawn 只保留第一个
```

### 执行流程示意

```
用户发送图片 + "帮我分析并执行xxx"
                ↓
    ┌───────────┴───────────┐
    ↓                       ↓
spawn(vision)          exec(图片命令)
    ↓ (先执行)          ↓ (后执行)
 图像分析完成           命令执行
```

### 实际收益

- 🔒 **执行安全**：避免并行冲突导致的失败
- 📊 **结果可靠**：确保 vision 分析结果可用于后续命令
- 🧩 **智能编排**：系统自动处理复杂场景

---

## ⏳ 3. 超时任务后台执行

### 问题背景

长时间运行的任务（如代码重构、大文件处理）可能超过预设的超时时间，传统做法是直接放弃任务，用户体验不佳。

### 解决方案

超时后任务继续在后台运行，完成后自动推送结果：

```python
except asyncio.TimeoutError:
    # 超时后任务受 shield 保护继续运行
    logger.info(f"[SubagentProgress] Task {task_id} timed out, waiting for late result...")
    partial = "⏳ 任务执行超时，正在后台继续运行，完成后将自动通知。"
    bus.push(origin_key, {...})
    
    # 任务完成后统一处理结果
    await _deliver_late_result(inner_task)
```

### 实际收益

- 🌙 **后台执行**：用户无需持续等待
- 🔔 **自动通知**：任务完成后主动推送结果
- 📊 **状态追踪**：超时也有清晰的进度反馈

---

## 🌐 4. Web UI SSE 重连机制

### 问题背景

用户在聊天过程中刷新页面或切换标签页，会导致 SSE 连接断开，无法继续接收实时推送。

### 解决方案

新增 **ChatStreamBus** 全局事件总线：

```python
class ChatStreamBus:
    """支持多订阅者按 origin_key 订阅事件，线程安全"""
    
    _MAX_BUFFER = 200  # 事件缓冲上限
    
    def subscribe(self, origin_key: str, replay: bool = True):
        """晚到的订阅者可回放已发生的事件"""
```

### 前端重连逻辑

```typescript
const tryReconnectChatStream = useCallback(async (sessionId: string) => {
    const result = await api.subscribeToChatStream(
        sessionId, 
        handleStreamEvent, 
        ctrl.signal
    );
    // 重新订阅后继续接收推送
});
```

### 实际收益

- 🔄 **无缝体验**：刷新页面不丢失实时消息
- 📡 **事件回放**：重新连接后自动补发遗漏事件
- 💾 **内存优化**：超过 200 条自动清理旧事件

---

## 🛠️ 5. 子 Agent 技能（Skills）配置

### 新增功能

现在可以为不同的子 Agent 模板配置特定的技能（Skills）：

```python
@dataclass
class AgentTemplate:
    name: str
    description: str
    tools: list[str]
    rules: list[str]
    system_prompt: str
    skills: list[str] = field(default_factory=list)  # 新增！
```

在构建子 Agent 系统提示时，自动注入对应技能：

```python
def build_system_prompt(self, name: str, task: str, workspace: str):
    base_prompt = template.system_prompt.format(...)
    
    if template.skills:
        skills_content = skills_loader.load_skills_for_context(template.skills)
        base_prompt += f"\n\n## 参考 Skills\n\n{skills_content}"
    
    return base_prompt
```

### 实际收益

- 🎯 **精细控制**：不同任务使用不同技能组合
- 🔧 **灵活扩展**：通过配置而非代码添加新能力
- 📦 **复用性高**：技能可在多个模板间共享

---

## ⚡ 6. 工具实例缓存

### 问题背景

之前每次 spawn 子 Agent 都会重新创建工具实例，造成不必要的开销。

### 解决方案

新增工具缓存机制：

```python
class SubagentManager:
    def __init__(self, ...):
        # 工具缓存：按模板缓存，避免每次 spawn 都重新创建
        self._tools_cache: dict[str, Any] = {}
```

### 实际收益

- 🚀 **启动更快**：复用已有工具实例
- 💾 **内存优化**：减少对象重复创建
- 📈 **吞吐量提升**：高并发场景表现更佳

---

## 🧹 7. 代码清理

- 移除 `nanobot/agent/tools/claude_code.py`（功能已整合到 SubagentManager）
- `.gitignore` 新增 `*.db` 规则

---

## 📊 总结

本次更新带来了显著的多维度提升：

### 性能提升
- Vision 模板去重 + 更低相似度阈值 → 减少重复 API 调用
- 工具实例缓存 → 减少对象创建开销
- Vision-Exec 串行化 → 避免执行冲突导致的失败重试

### 拓展性增强
- 子 Agent 技能配置 → 支持更精细的任务定制
- ChatStreamBus 架构 → 为未来功能扩展奠定基础

### 文档与可维护性
- 详细日志记录 → 问题排查更便捷
- 统一的代码结构 → 后续维护更简单

---

## 🚀 如何升级

```bash
cd E:\workSpace\nanobot-webui
git pull
# 重启服务即可体验新功能
```

如果你在使用过程中遇到任何问题，欢迎在 GitHub 提 Issue 或加入我们的社区讨论！

**Happy Coding!** 🐈
