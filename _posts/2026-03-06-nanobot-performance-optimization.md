---
layout: post
title: "nanobot-webui 性能与扩展性优化：子Agent批量处理、执行链路监控与智能并行"
date: 2026-03-04
tags: [nanobot, AI Agent, 性能优化, 飞书, Python]
author: Chris
---

最近对 nanobot-webui 进行了一系列重要的性能与扩展性优化，本文将详细介绍这些改进如何提升系统性能、可维护性和用户体验。

## 一、子Agent批量处理优化

### 1.1 批量任务聚合机制

在实际业务场景中，我们经常需要同时触发多个子Agent来并行处理不同任务。之前的版本虽然支持子Agent，但每个任务都是独立完成、单独通知，无法满足批量处理的需求。

本次优化引入了 **batch_id 机制**：

```python
# 核心数据结构
self._batch_tasks: dict[str, set[str]] = {}  # batch_id -> set[task_id]
self._batch_lock = threading.Lock()
```

当调用 `spawn` 方法时，可以传入相同的 `batch_id`，系统会自动追踪同一批次的所有任务：

```python
# 批量spawn多个子Agent
task_id_1 = await subagent_manager.spawn(
    task="分析代码文件 A",
    batch_id="batch_001"
)
task_id_2 = await subagent_manager.spawn(
    task="分析代码文件 B", 
    batch_id="batch_001"
)
```

### 1.2 智能汇总与交付

当同一个 batch 中的所有任务完成后，系统会触发汇总机制：

- **Web 渠道**：调用 LLM 生成综合 summary，推送到 `SubagentProgressBus`，前端可以一次性展示所有结果
- **非 Web 渠道**（如飞书）：将所有结果合并为一条系统消息，注入主 agent 进行自然语言回复

```python
async def _deliver_batch_complete(self, batch_id, batch_task_ids, origin):
    """batch 内所有任务完成，进行汇总并交付"""
    # 构建完整任务+结果内容
    combined_preview = "\n\n---\n\n".join(preview_parts)
    
    # 使用 LLM 进行智能汇总
    response = await self.provider.chat(
        messages=[...],
        model=self._main_model,
    )
```

### 1.3 工具缓存优化

为了避免每次 spawn 都重新创建工具实例，引入了工具缓存机制：

```python
# 工具缓存：按模板缓存
self._tools_cache: dict[str, Any] = {}

def _create_tools_for_template(self, template: str) -> ToolRegistry:
    # 检查缓存
    if template in self._tools_cache:
        return self._tools_cache[template]
    
    # 创建工具实例并缓存
    tools = ToolRegistry()
    # ... 注册工具 ...
    self._tools_cache[template] = tools
    return tools
```

## 二、执行链路监控

### 2.1 ExecutionChainMonitor 集成

为了更好地追踪和调试 Agent 的执行过程，引入了执行链路监控：

```python
# 初始化执行链路监控
from nanobot.monitoring.execution_chain import ExecutionChainMonitor
self._chain_monitor = ExecutionChainMonitor.get_instance()

# 创建子 Agent 执行节点
subagent_node = self._chain_monitor.get_current_chain().create_node(
    node_type='subagent',
    name=template,
    parent_node_id=parent_node_id,
    arguments={'task': task, 'label': label}
)
```

### 2.2 节点状态追踪

每个工具调用和子Agent都会创建对应的执行节点，记录：

- 节点类型（subagent / tool）
- 节点参数
- 执行结果
- 执行时间
- 错误信息

这为后续的性能分析和问题排查提供了有力支持。

## 三、智能并行执行

### 3.1 Vision-Exec 冲突检测

当用户同时发送图片并要求执行命令时，存在 vision 子Agent 和 exec 工具冲突的风险：

```python
def _resolve_vision_exec_groups(self, tool_calls, image_files):
    """
    检测 spawn(vision) + exec(图片相关) 冲突，返回串行分组（vision 先行）
    """
    # 分离不同类型的工具调用
    spawn_vision = []   # 视觉分析任务
    exec_image = []     # 图片相关命令
    others = []         # 其他任务
    
    # 串行组：vision 先行，再 exec
    group1 = vision_deduped + exec_image
    return [group1] + [[tc] for tc in others]
```

### 3.2 Spawn 语义去重

为了避免同一轮对话中重复执行相似的任务，引入了语义相似度检测：

```python
def _spawn_tasks_similar(self, task_a: str, task_b: str, threshold: float = 0.78):
    """判断两个 spawn task 是否语义相似"""
    na, nb = self._normalize_spawn_task(task_a), self._normalize_spawn_task(task_b)
    ratio = difflib.SequenceMatcher(None, na, nb).ratio()
    return ratio >= threshold

def _is_duplicate_spawn(self, spawn_args, tool_steps):
    """检查是否已执行过语义相似的 spawn"""
    # vision 模板：本回合已有任一 vision spawn 即视为重复
    if new_template == "vision":
        if any(s.get("name") == "spawn" and ...):
            return True
```

### 3.3 智能并行决策器

引入了 `SmartParallelDecider` 来智能判断是否需要并行执行：

```python
# 初始化智能并行判断器
self._smart_parallel_decider = SmartParallelDecider(
    provider=provider,
    model=smart_parallel_model,
    use_simple_prompt=True,
)

# 智能判断
decision = await self._smart_parallel_decider.should_parallel(tool_calls)
should_parallel = decision.get("parallel", True)
```

## 四、性能优化细节

### 4.1 取消机制优化

支持按 session 取消子Agent任务，实现真正的停止执行：

```python
def cancel_by_session(self, channel: str, chat_id: str) -> int:
    """取消指定 session 的所有子代理任务"""
    origin_key = f"{channel}:{chat_id}"
    self._session_cancelled.add(origin_key)
    
    # 遍历所有运行中的任务
    for task_id, (orig_key, _) in list(self._running_tasks.items()):
        if orig_key == origin_key:
            self._running_tasks.pop(task_id, None)
            cancelled += 1
```

### 4.2 LLM 调用取消轮询

在 LLM 调用期间每 2 秒轮询取消状态，与主 Agent 一致：

```python
_LLM_CALL_TIMEOUT = 120
_CANCEL_CHECK_INTERVAL = 2.0

while not llm_task.done():
    elapsed = time.monotonic() - loop_start
    remaining = _LLM_CALL_TIMEOUT - elapsed
    
    # 每 2 秒检查一次取消状态
    if origin_key in self._session_cancelled:
        llm_task.cancel()
        cancelled_during_llm = True
        break
```

### 4.3 线程池资源管理

使用线程池执行 CPU 密集型任务，避免阻塞事件循环：

```python
# 初始化线程池
self._thread_pool_executor = ThreadPoolExecutor(max_workers=self._thread_pool_size)

# 判断是否需要线程池
use_thread_pool = tool_call.name in self._thread_pool_tools
if use_thread_pool and self._thread_pool_executor:
    result = await self.tools.execute_in_thread_pool(
        tool_call.name,
        tool_call.arguments,
        self._thread_pool_executor
    )
```

## 五、扩展性增强

### 5.1 BackendRegistry 架构

引入后端注册机制，支持灵活扩展不同的执行后端：

```python
# Backend registry and resolver
from nanobot.agent.backend_registry import BackendRegistry
from nanobot.agent.backend_resolver import BackendResolver

self._backend_registry = BackendRegistry()
self._backend_resolver = BackendResolver(
    agent_template_manager, 
    self._backend_registry
)

# 自动路由到对应后端
runner = self._backend_registry.get(effective_backend)
if runner is not None:
    await runner(task_id, task, label, origin, ...)
```

### 5.2 懒加载 MCP 工具

MCP 工具采用懒加载模式，按需建立连接：

```python
def _init_mcp_loader(self) -> None:
    """Initialize MCP tool loader - 按需加载模式"""
    # 只注册工具代理，不建立任何连接
    for mcp_cfg in mcps:
        adapter = McpLazyToolAdapter(
            server_id=server_id,
            tool_name=tool_name,
            mcp_loader=self.mcp_loader,
        )
        self.tools.register(adapter)
```

### 5.3 Agent 模板 UI 配置化

通过前端界面可视化管理 Agent 模板：

```typescript
interface AgentTemplate {
  name: string;           // 模板名称
  description: string;    // 简短描述
  model?: string;         // 指定使用的模型
  tools: string[];        // 可用工具列表
  skills?: string[];      // 引用的 Skills
  rules: string[];        // 行为规则
  system_prompt: string;   // 系统提示词
}
```

## 六、文档与日志优化

### 6.1 详细的执行日志

每个关键操作都有详细的日志记录：

```python
logger.info(f"[SubagentProgress] SubagentManager id: {id(self)}")
logger.info(f"[ExecutionChain] Created subagent node: {subagent_node_id}")
logger.info(f"[ToolExecution] Tool '{tool_call.name}' completed in {execution_time:.2f}s")
```

### 6.2 进度事件推送

通过 `SubagentProgressBus` 将进度事件推送给前端：

```python
bus.push(origin_key, {
    "type": "subagent_progress",
    "task_id": task_id,
    "subtype": subtype,
    "content": content,
    "tool_name": payload.get("tool_name"),
})
```

## 总结

本次更新带来了多维度的优化：

| 优化维度 | 改进内容 |
|---------|---------|
| **性能** | 工具缓存、线程池、LLM取消轮询 |
| **扩展性** | BackendRegistry、懒加载MCP、模板UI配置化 |
| **可维护性** | 执行链路监控、详细日志、进度事件 |
| **用户体验** | 批量任务聚合、智能并行、语义去重 |

这些改进使得 nanobot-webui 能够更高效地处理复杂的多任务场景，同时保持了良好的可扩展性和可维护性。
