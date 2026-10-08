# Claude Code：有边界的源码阅读索引

[案例七](../cases/07-claude-code-runtime.md) · [案例八](../cases/08-claude-code-collaboration.md) · [案例九](../cases/09-claude-code-source-reading.md) · [学习路线](../README.md)

核对日期：**2026-10-08**。以下是阅读与来源判断，不是运行测评、安全审计或采用建议。官方文档描述当前接口；固定提交只描述该版本的公开组件。没有把第三方解析中的私有实现当作官方开源代码。

## 官方 Python SDK：从边界读起

来源：[anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python)。固定提交：`f7b0b62c2a8d110d4da0eec0aa70cf795ec3afc4`（2026-10-07；提交说明将 bundled CLI 更新至 2.1.293）。

推荐顺序：

1. [query.py](https://github.com/anthropics/claude-agent-sdk-python/blob/f7b0b62c2a8d110d4da0eec0aa70cf795ec3afc4/src/claude_agent_sdk/query.py)：应用怎样开始请求、接收消息？
2. [subprocess_cli.py](https://github.com/anthropics/claude-agent-sdk-python/blob/f7b0b62c2a8d110d4da0eec0aa70cf795ec3afc4/src/claude_agent_sdk/_internal/transport/subprocess_cli.py)：谁启动 CLI、设置工作目录、管理输入输出和退出？
3. [_internal/query.py](https://github.com/anthropics/claude-agent-sdk-python/blob/f7b0b62c2a8d110d4da0eec0aa70cf795ec3afc4/src/claude_agent_sdk/_internal/query.py)：为什么消息流还需要控制请求、响应 ID 和取消？

**能学到：** 封装层、进程边界、流式事件和控制协议。**不能推出：** 私有核心模型/工具循环的完整实现。

该仓库代码有 [MIT 许可证](https://github.com/anthropics/claude-agent-sdk-python/blob/f7b0b62c2a8d110d4da0eec0aa70cf795ec3afc4/LICENSE)，README 另说明使用条款；不要把 Python 源码许可证扩展到打包的 CLI。SDK 的 `allowed_tools` 是自动批准列表，不能当作工具可见性的完整白名单。

## 官方 Sandbox Runtime：读执行边界

[anthropics/sandbox-runtime](https://github.com/anthropics/sandbox-runtime/tree/3f0bad7345238f47736435e3f2b064399c1cad74)，固定提交 `3f0bad7345238f47736435e3f2b064399c1cad74`，Apache-2.0；项目自述为研究预览。

先读 README 的文件系统和网络隔离，再追对应平台实现。它展示模型以下的操作系统约束，适合回答“获准运行的命令还能访问什么”。它是官方公开组件，不是整个 Claude Code；不能仅从这个仓库推断某个安装版本采用的全部配置。

## 官方 Agent SDK demos：读应用怎样包住运行时

[anthropics/claude-agent-sdk-demos](https://github.com/anthropics/claude-agent-sdk-demos)。选择一个例子，寻找输入、SDK 调用、事件显示和结果保存四处边界。

它适合学习应用集成，不是 CLI 内部源码。各示例依赖和许可需分别核对；本教程没有安装或执行。这里使用访问日期而非固定提交，不作逐行实现结论。

## 第三方双语解析：当成问题清单

[How Claude Code Works](https://github.com/Windy3f3f3f3f/how-claude-code-works) 是独立教育性解析，不隶属 Anthropic。作者声明不保证与真实内部实现一致，也不分发 Anthropic 源码；README 另提及社区快照及持续逆向分析，含 2026-07-04 更新说明。

可借它提出“上下文怎样增长”“工具结果怎样回来”等问题，再查官方证据。不要直接继承其性能数字、设计动机或当前功能判断。其关联的教育重写即使声称 clean-room，也应作为独立项目阅读，而非官方实现。

## 独立论文：看版本与证据分层

[Dive into Claude Code，arXiv v2](https://arxiv.org/abs/2604.14228v2)，Liu 等，2026-07-02 修订；[正文](https://arxiv.org/html/2604.14228v2)。分析主体是 **v2.1.88 快照**，不是今天安装版本的完整说明。

值得学的是区分官方材料、重建分析和推断。作者也指出，静态代码不能证明设计意图、线上启用的功能开关或实际使用频率。论文中的目录、函数和数量应标注为该研究的观察，不能由论文反推官方已经授权开源。

## 版本陷阱：读旧教程前检查这几项

- **嵌套 subagent：** 当前官方默认三层；v2.1.172–216 曾是五层，v2.1.217–218 默认一层，v2.1.219 调整为三层。[官方版本说明](https://code.claude.com/docs/en/sub-agents#let-subagents-spawn-their-own-subagents)
- **Dynamic workflows：** 当前文档提供脚本编排，不能仍把全部调度描述成模型逐轮决定。当前覆盖付费计划、API 和列明的云提供方；Pro 需在 `/config` 开启。检查自己版本和模式。[官方说明](https://code.claude.com/docs/en/workflows)
- **跨会话通信：** macOS/Linux 从 v2.1.224 起，原生 Windows 从 v2.1.234 起；发送的是文本，接收方权限仍有效。[官方说明](https://code.claude.com/docs/en/cross-session-messaging)
- **Agent teams：** 实验、默认关闭、需要交互会话；有消息能力不自动代表启动了 team。恢复主会话不恢复 in-process teammates。[官方说明](https://code.claude.com/docs/en/agent-teams)
- **持续等待：** `/loop`、Desktop scheduled tasks、Cloud routines 的机器和会话要求不同；恢复部分调度记录不等于离线期间一直执行。[官方比较](https://code.claude.com/docs/en/scheduled-tasks#compare-scheduling-options)

## 公开、可读、开源分别核对

[claude-code 根许可](https://github.com/anthropics/claude-code/blob/main/LICENSE.md) 和 [TypeScript SDK 根许可](https://github.com/anthropics/claude-agent-sdk-typescript/blob/main/LICENSE.md) 均保留权利并指向商业条款。不能因为仓库存在、npm 能下载或某个镜像贴了许可，就把核心运行时称为完整开源。

本教程优先链接官方公开组件和原创分析，不复制私有核心源码，不把来源未核实的“泄露”“重构”“移植”仓库当作权威依据。
