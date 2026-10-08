# 19 消息 调用与控制权交接

[上一课](18-manager-and-tools.md) · [学习路线](../README.md) · [下一课](20-parallel.md)

## 三种看起来相似的动作

“请审查这份 diff，再把结果给我”是子任务调用。

“发现一个新风险，先告诉负责人工单可能要改范围”是消息通知。

“接下来由验收助手与你澄清怎么验收”是对话控制权交接。

它们都可能涉及两个 Agent，但返回方式和责任完全不同。

## SDK 中的 handoff

OpenAI Agents SDK 可以用 `handoff` 让另一个 Agent 成为当前运行的 active agent，即接下来负责继续对话的 Agent。

```python
from agents import Agent, handoff

acceptance = Agent(
    name="Acceptance assistant",
    model=MODEL,
    instructions="澄清验收步骤，记录明确反馈，不代替用户批准发布。",
)

triage = Agent(
    name="Engineering triage",
    model=MODEL,
    instructions="需要澄清人工验收步骤时，交给 Acceptance assistant。",
    handoffs=[handoff(acceptance)],
)
```

这是未运行的 API 片段。[官方 handoff 文档](https://openai.github.io/openai-agents-python/handoffs/)

这里没有启动一个并行后台 reviewer。交接后由接收者继续当前 run。若只想问专家一个问题，再由管理者接着处理，上一课的工具式调用更直观。

## 运行时交接不等于业务责任全部转移

框架切换当前 Agent，只解决了一部分控制问题。你的应用仍要决定：谁对工单负责、谁能执行哪些动作、何时返回、卡住时向谁升级。

也不能假定交接会自动只传你期望的三句话。有些框架会提供历史过滤机制。使用 SDK 时应明确检查接收者看到哪些历史；业务权限则应来自可信运行上下文，而不是模型写在交接原因里的文字。

## 人与 Agent 之间也需要交接包

一个有用的交接包可以只用七行：

1. 当前目标及完成标准。
2. 当前产物与版本。
3. 已验证事实及证据。
4. 已尝试但失败的路径。
5. 仍需解决的问题。
6. 接收方允许做的动作。
7. 接收后何时返回或升级。

如果采用异步团队消息，还要明确接收确认。消息已发出不代表对方已接管。在接管前，原负责人不应悄悄放弃责任。

## 小练习

“测试专家帮忙看一下”究竟是哪一种动作？信息不足。改写成一个明确的子任务调用，再改写成一个明确交接，比较两者结束条件。

**带走一句话：传递信息 调用能力和转移控制权，是三个不同的协议。**
