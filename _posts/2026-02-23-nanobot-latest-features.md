---
layout: post
title: "nanobot：功能全面升级的AI助手"
date: 2026-02-23 00:00:00 +0800
categories: AI开发
tags: [nanobot, AI助手, 开源项目, 多平台, LLM, 技能系统]
author: 技术博主
read_time: 约8分钟
---

> 在AI技术飞速发展的今天，拥有一个强大且灵活的個人AI助手已成为提升工作效率的关键。nanobot作为一款功能全面的开源AI助手，近期完成了重大版本升级，带来了更丰富的功能和更友好的使用体验。今天就让我们一起深入了解这款工具的最新能力。

## 什么是nanobot？

nanobot是一个基于大语言模型的个人AI助手框架，以约4000行核心代码实现了完整的Agent功能。它受Clawdbot启发，采用轻量级架构设计，同时保持了强大的可扩展性。最新的nanobot-webui版本在此基础上增加了现代化的Web管理界面和多平台支持，让AI助手的使用变得更加简单直观。

## 多平台支持：随时随地与AI对话

nanobot支持多种平台接入，你可以根据自己的使用场景选择最方便的方式：

- **Web UI** - 现代化Web管理界面
- **Telegram** - 即时通讯平台
- **飞书** - 企业协作平台
- **Discord** - 社区交流平台
- **QQ** - 国内主流即时通讯
- **钉钉** - 企业办公平台
- **CLI** - 命令行界面

### Web UI界面

nanobot-webui提供了功能完备的React单页应用界面，主要包括：

- **聊天界面** - 支持Markdown渲染、多轮对话、会话历史管理
- **文件浏览器** - 直接在界面中浏览和管理工作区文件
- **配置管理** - 轻松管理Channels、Providers、Models、MCP服务和Skills
- **系统状态** - 实时查看服务健康状态、运行时长、会话数量

### 命令行界面

对于开发者而言，CLI模式同样支持完善的功能：

```bash
# 初始化配置
nanobot onboard

# 与AI对话
nanobot agent -m "帮我写一个Python脚本"

# 启动Web界面
nanobot web-ui
```

## 多种大语言模型支持

nanobot不依赖特定的AI模型服务商，支持灵活切换：

| 模型 | 说明 |
|------|------|
| DeepSeek | 国产优秀的大模型，性价比高 |
| OpenAI | GPT-4o、GPT-4 Turbo等 |
| Anthropic Claude | Claude 3.5 Sonnet等 |
| 阿里通义千问 | Qwen系列模型 |
| 智谱GLM | 清华技术背景的国产大模型 |
| Google Gemini | Google的多模态大模型 |
| OpenRouter | 统一接入多种模型 |
| vLLM | 本地部署大模型 |

更重要的是，nanobot支持**本地运行**，所有数据都存储在本地，保护用户隐私安全。你可以选择使用本地部署的模型，享受完全的数据控制权。

## 核心功能模块

### 文件系统操作

nanobot具备完整的文件系统操作能力，可以：

- 读取和写入文件
- 创建、删除和移动文件/目录
- 搜索文件内容
- 批量处理文件

### 代码执行能力

通过集成的代码执行环境，nanobot可以：

- 编写和运行Python、JavaScript等代码
- 执行Shell命令
- 实时调试和分析代码

### 记忆系统

nanobot的记忆系统是其核心亮点之一：

- **长期记忆** - 跨会话记住用户的偏好设置、重要信息
- **每日笔记** - 自动记录每天的交互内容
- **上下文保持** - 在多轮对话中保持连贯的上下文理解

### 技能系统（Skills）

nanobot的可扩展技能系统让它能够完成更复杂的任务。目前内置了8个强大的技能：

| 技能 | 功能描述 |
|------|----------|
| claude-code | 委托编码任务给Claude Code CLI，用于高级代码生成和重构 |
| git-manager | Git仓库管理 — 提交、推送、拉取、分支操作 |
| xlsx | Excel电子表格操作 — 读取、写入、编辑.xlsx文件 |
| pdf | PDF操作 — 读取、写入、合并、分割PDF文档 |
| pptx | PowerPoint演示文稿操作 — 创建和编辑.pptx文件 |
| skill-creator | 创建新技能以扩展nanobot的能力 |
| mirror-system | 自我认知探索系统，助力个人成长 |
| code-review-expert | Git diff代码审查 — 分析变更并提供专业反馈 |

## MCP协议支持

nanobot还支持Model Context Protocol (MCP)，可以接入丰富的外部工具和服务：

- **stdio模式** - 本地进程通信
- **HTTP模式** - 网络API调用
- **SSE模式** - 服务端推送
- **streamable_http模式** - 流式HTTP通信

通过MCP，nanobot可以连接各种外部服务，比如天气API、数据库、搜索引擎等，大大扩展了其实用性。

## 实际使用场景

> **场景一：日常办公自动化**
> 通过xlsx技能快速处理Excel报表，用pptx技能自动生成演示文稿，用pdf技能批量处理文档。

> **场景二：代码开发辅助**
> 使用claude-code进行高级代码生成，利用code-review-expert进行代码审查，通过git-manager管理代码版本。

> **场景三：团队协作**
> 集成到飞书或钉钉，作为团队的知识问答助手，统一管理多渠道的AI服务。

> **场景四：个人知识管理**
> 利用记忆系统记录学习笔记，通过mirror-system进行自我反思和成长规划。

## 快速开始

### 安装部署

```bash
# 克隆项目
git clone https://github.com/codemo1991/nanobot-webui.git
cd nanobot-webui
pip install -e .
```

### 一键启动（推荐）

- **Windows：** 双击 `startup.bat`
- **Linux/macOS：**
  ```bash
  chmod +x startup.sh
  ./startup.sh
  ```

### Docker部署

```bash
# 构建镜像
docker build -t nanobot-webui .

# 启动容器
docker run -d -p 6788:6788 -v nanobot-data:/root/.nanobot --name nanobot nanobot-webui
```

启动后访问 [http://127.0.0.1:6788](http://127.0.0.1:6788) 即可开始使用。

> **首次使用提示**
> 首次启动后，系统会自动创建配置文件 `~/.nanobot/config.json`。你可以在Web界面的配置页面中添加AI模型的API Key，支持各大主流模型服务商。

## 未来展望

nanobot项目仍在持续迭代中，未来计划包括：

- **更多内置技能** - 数据分析、图像处理等实用技能
- **插件系统** - 更灵活的可扩展机制
- **多语言支持** - 更完善的国际化
- **移动端适配** - 更友好的移动端体验

## 总结

nanobot作为一款功能全面的开源AI助手，凭借其轻量级的架构、丰富的内置技能、多平台支持和灵活的配置选项，为用户提供了一个强大而实用的个人AI助手解决方案。

无论你是想提升个人工作效率的开发者，还是需要团队协作工具的企业用户，nanobot都值得一试。其开源的特性也让用户可以完全掌控自己的数据，真正实现了AI助手的私有化部署。

项目地址：[https://github.com/codemo1991/nanobot-webui](https://github.com/codemo1991/nanobot-webui)

---

> **个人感受**：使用nanobot已经有一段时间了，最让我惊喜的是它的技能系统。特别是xlsx和pptx技能，大大提升了我处理日常办公文档的效率。加上记忆系统的加持，AI助手越来越"懂我"，推荐各位也试试看！
