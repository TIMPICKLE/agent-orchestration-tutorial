# 22 通知也是需要管理的动作

[上一课](21-triggers.md) · [学习路线](../README.md) · [下一课](23-human-approval.md)

## 子 Agent 可以先报告再继续

假设调查者发现工单描述与实际代码不一致。它不必等整项调查结束才报告，但“报告”需要一个真正的工具或消息接口。

下面使用 OpenAI Agents SDK 的工具装饰器说明结构。代码未运行；这里的列表只是内存演示，不能抗崩溃，也不会真正发送消息。

```python
from dataclasses import dataclass, field
from agents import RunContextWrapper, function_tool

@dataclass
class Context:
    task_id: str
    outbox: list[dict] = field(default_factory=list)

@function_tool
async def notify_coordinator(
    ctx: RunContextWrapper[Context],
    summary: str,
) -> str:
    """向当前任务的固定主管报告重要进展。"""
    ctx.context.outbox.append({
        "task_id": ctx.context.task_id,
        "kind": "worker_update",
        "summary": summary,
    })
    return "queued"
```

还需把该工具注册到 worker 的 `tools`，运行时传入 `Context`，并实现 outbox 消费者。装饰器并没有自动完成这些应用工作。[官方工具接口](https://openai.github.io/openai-agents-python/tools/)

## queued 只表示排入待处理列表

`outbox` 可以译成待发箱。模型选择调用工具，工具登记消息，消费者负责投递。这三步是不同职责。

如果消费者不存在，消息永远不会到主管那里。如果主管没有新一轮运行，也不会仅因列表多了一项就自动理解更新。

对于普通同步专家调用，直接返回结果已经足够。只有确实需要提前通知或后台协作时，才引入额外消息机制。

## 对用户通知还要多做一层判断

不是每条工具日志都值得打断人。可以把通知分为：需要用户决定、关键阻塞、任务完成、普通进度。前几类通常更有价值，普通进度可合并展示。

同时核对接收者、渠道许可、内容范围和重复通知。固定目标通常比允许模型任意输入邮箱或频道更容易控制。

消息内容也应区分“已提交发送”“服务确认接收”“已送达”“已读”。平台不提供哪个回执，就不要编造哪个状态。

## 把第 08 课的问题补齐

真实待发箱需要持久保存和稳定消息标识。发送超时后先核对结果，再选择安全重试。数据库记录和外部发送之间仍可能存在不确定窗口。

[离线消息实验](../examples/message_delivery.py) 用假接收服务演示这个问题，帮助你观察“发送成功但回复丢失”的恢复；它不能证明所有真实平台都提供相同的去重能力。

## 小练习

worker 连续十次报告同一个阻塞，用户还没回复。你会十次都发提醒吗？写一个按任务、阻塞类型和当前证据版本去重的规则，同时保留真正的新变化。

**带走一句话：模型可以提出通知，可靠送达和是否值得打扰由应用一起负责。**
