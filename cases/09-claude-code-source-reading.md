# 案例九 怎样读 Claude Code 的公开代码与解析

[运行原理](07-claude-code-runtime.md) · [协作案例](08-claude-code-collaboration.md) · [学习路线](../README.md)

## 第一步先问：眼前究竟是什么

搜索“Claude Code 源码”会遇到官方仓库、SDK、构建产物、第三方解析和重写项目。它们能回答的问题不同。

[官方 claude-code 仓库](https://github.com/anthropics/claude-code) 公开提供插件、说明和变更记录；本次检查未发现完整核心运行时源码树。[根许可证](https://github.com/anthropics/claude-code/blob/main/LICENSE.md) 保留权利并指向商业条款。**仓库公开，不等于核心运行时已经开源。**

## 从一个能验证的小问题开始

问题：“Python 应用调用 Agent SDK 后，工作在哪一层执行？”

1. 读官方 Python SDK 的 `query` / client 入口，确认应用接收什么消息。
2. 追到 `subprocess_cli.py`，找 CLI 进程启动和输入输出管道。
3. 再读 `_internal/query.py`，看普通消息与双向控制请求怎样分流。

这样可以验证 **SDK 与 CLI 的边界**，不必先相信一幅庞大的“内部架构图”。但 SDK 中名为 `query` 的文件，不等于公开了 Claude Code 私有核心循环。[固定版本源码路线](../references/claude-code-reading.md#官方-python-sdk从边界读起)

## 解析文章怎样读才有用

把文章中的结论分成三类：能在官方接口核对的行为、作者对特定版本的代码观察、作者对设计动机的解释。后一类即使很合理，也不能写成官方保证。

例如一份第三方报告分析 v2.1.88，而当前官方文档已说明之后的嵌套 subagent 和 dynamic workflows。旧报告仍能启发设计问题，但不能据此否定新功能。[带出处的五项阅读资源](../references/claude-code-reading.md)

教学重写也有价值：你可以运行并修改它，观察自己的工具循环。但它证明的是这个重写如何工作，不能用它给 Claude Code 的真实内部实现作证。可下载的 bundle、来源未核实的源码快照和官方授权开源是不同事实。

## 一个三行读书记录

- 我看到的事实：SDK 启动 CLI 子进程并读取消息。
- 我的解释：产品把嵌入接口与执行运行时分开，调用者不必重写全部工具系统。
- 仍待验证：某个运行模式下，子任务何时结束、哪些状态可以恢复。

把这三行分开，才容易发现证据缺口。本页从官方组件与第三方解析建立阅读方法；进一步阅读公开历史快照中的实际核心循环，请接着看[案例十](10-historical-query-loop.md)和[历史阅读索引](../references/claude-code-historical-reading.md)。本教程发布原创分析与来源链接，不复制历史源码树，也没有执行下载包或审计完整产品。

**带走一句话：先确定来源与版本，再沿一个具体问题读代码；不要让“源码解析”四个字代替证据。**
