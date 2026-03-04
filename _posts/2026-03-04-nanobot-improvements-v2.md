---
layout: post
title: "nanobot-webui 三大核心改进：子Agent批量处理、语音支持与UI配置化"
date: 2026-03-04
tags: [nanobot, AI Agent, 飞书, Claude Code]
author: Chris
---

最近对 nanobot-webui 进行了一系列重要升级，本文将详细介绍这三个核心改进：**子Agent批量处理优化**、**语音消息支持**以及**Agent模板UI配置化**。

## 一、子Agent批量处理优化

### 1.1 背景与需求

在实际使用中，我们经常需要同时触发多个子Agent来并行处理不同任务。例如：
- 同时分析多封邮件
- 并行搜索多个关键词
- 同时处理多个文件的代码审查

之前的版本虽然支持子Agent，但每个任务都是独立完成、单独通知，无法满足批量处理的需求。

### 1.2 实现原理

在 `SubagentManager` 中引入了 `batch_id` 机制：

```python
# 核心数据结构
self._batch_tasks: dict[str, set[str]] = {}  # batch_id -> set[task_id]
self._batch_lock = threading.Lock()
```

当调用 `spawn` 方法时，可以传入相同的 `batch_id`：

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

### 1.3 聚合汇总机制

当同一个 batch 中的所有任务完成后，系统会触发 `_deliver_batch_complete` 方法进行汇总：

**Web 渠道**：调用 LLM 生成综合 summary，推送到 `SubagentProgressBus`，前端可以一次性展示所有结果。

```python
async def _generate_batch_summary(self, batch_id, batch_results, origin):
    # 构建完整的任务+结果内容
    combined_preview = "\n\n---\n\n".join(preview_parts)
    
    # 使用 LLM 进行智能汇总
    response = await self.provider.chat(
        messages=[
            {"role": "system", "content": BATCH_SUMMARY_SYSTEM},
            {"role": "user", "content": summary_prompt},
        ],
        model=self._main_model,
    )
```

**非 Web 渠道**（如飞书）：将所有结果合并为一条系统消息，注入主 agent 进行自然语言回复。

### 1.4 使用示例

```python
# 批量代码审查
batch_id = "code_review_batch"
for file in code_files:
    await subagent_manager.spawn(
        task=f"审查文件 {file}，关注安全性、性能和最佳实践",
        template="code-review",
        batch_id=batch_id,
        origin_channel="feishu",
        origin_chat_id=chat_id
    )
```

## 二、Voice 语音发送支持

### 2.1 飞书语音消息处理

nanobot 现在可以完整支持飞书语音消息：

```python
# 接收语音消息
elif msg_type == "audio":
    audio_path = await self._download_audio_from_message(
        message_id, message.content
    )
    if audio_path:
        media_paths.append(audio_path)
        content_parts.append("[语音]")
```

### 2.2 语音转写流程

通过子Agent的 `voice` 模板，可以直接调用语音转写能力：

```python
# voice 模板专用处理：直接调用语音转写，绕过LLM
if template == "voice" and media and not self._media_has_images(media):
    audio_path = audio_paths[0]
    result = await tools.execute("voice_transcribe", {"file_path": audio_path})
    if result and not str(result).strip().startswith("Error:"):
        final_result = str(result).strip()
```

支持的音频格式：**mp3, wav, ogg, m4a, opus, webm, aac**

### 2.3 语音处理结果注入

转写完成后，可以将文本作为用户消息注入主agent：

```python
async def _inject_voice_as_user_message(self, origin, transcribed_text):
    msg = InboundMessage(
        channel=origin["channel"],
        sender_id="voice",
        chat_id=origin["chat_id"],
        content=transcribed_text.strip(),
    )
    await self.bus.publish_inbound(msg)
```

这使得用户可以直接发送语音，nanobot 会：
1. 下载语音文件
2. 调用 DashScope API 进行转写
3. 将转写文本作为用户消息
4. 主 agent 自动回复

## 三、Agent模板 UI 配置化

### 3.1 模板管理界面

通过前端 `AgentTemplatePage.tsx`，可以可视化管理 Agent 模板：

- **创建模板**：指定名称、描述、模型、工具、Skills、规则和系统提示词
- **编辑模板**：修改已有模板的配置
- **删除模板**：移除用户定义的模板
- **导入/导出**：支持 YAML 格式的批量导入导出

### 3.2 模板配置项

```typescript
interface AgentTemplate {
  name: string;           // 模板名称
  description: string;     // 简短描述
  model?: string;          // 指定使用的模型
  tools: string[];         // 可用工具列表
  skills?: string[];       // 引用的 Skills
  rules: string[];         // 行为规则
  system_prompt: string;   // 系统提示词
  enabled: boolean;        // 是否启用
}
```

### 3.3 工具选择

前端集成了所有可用的工具供选择：

- `read_file` / `write_file` / `edit_file` - 文件操作
- `list_dir` - 目录浏览
- `exec` - 命令执行
- `web_search` / `web_fetch` - 网页搜索
- `voice_transcribe` - 语音转写
- `claude_code` - Claude Code 集成

### 3.4 系统提示词预览

编辑器支持 Markdown 实时预览：

```tsx
<Segmented
  value={markdownPreview}
  onChange={(val) => setMarkdownPreview(val)}
  options={[
    { value: 'edit', label: '编辑' },
    { value: 'preview', label: '预览' }
  ]}
/>
```

支持的占位符：
- `{task}` - 当前任务描述
- `{all_rules}` - 所有规则内容
- `{workspace}` - 工作目录路径

### 3.5 YAML 导入导出

支持批量管理模板：

```yaml
# example-template.yaml
- name: my-coder
  description: 代码编写助手
  model: qwen-plus
  tools:
    - read_file
    - write_file
    - exec
    - web_search
  rules:
    - 遵循项目代码规范
    - 使用 TypeScript
  system_prompt: |
    你是一个专业的代码编写助手...
```

## 总结

这三个改进大幅提升了 nanobot-webui 的实用性：

1. **批量处理**让并行任务管理更加高效，特别适合需要同时处理多个相似任务的场景
2. **语音支持**让用户可以通过语音与 AI 助手交互，尤其适合移动场景
3. **UI配置化**降低了使用门槛，用户无需修改代码即可定制自己的 Agent 模板

这些功能已经集成到最新版本中，欢迎大家升级体验！
