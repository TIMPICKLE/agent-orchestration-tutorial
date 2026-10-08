# 完整框架装配示意

[学习路线](../README.md) · [离线可运行实验](../examples/README.md)

这些文件把正文短片段补成完整结构，便于检查变量、节点、工具和调用如何连接。它们**没有通过框架集成或真实模型测试**。语法验证状态见 [总验证记录](../references/verification.md)。

若你只想运行已经验证的教学实验，请先使用 `examples/`，那里仅依赖 Python 标准库。

## LangGraph

[langgraph_complete.py](langgraph_complete.py) 对应第 14–16 课。

文件包括：完整 State、attempt 初值与递增、两个预写候选、实际本地测试函数、条件路由、阻塞出口、内存 checkpointer、第一次调用、暂停后的状态读取，以及 `Command(resume=...)`。

在自行准备好兼容的 LangGraph 环境后，从仓库根目录运行：

```bash
python -m framework_samples.langgraph_complete
```

按代码设计，应该先看到待审阅状态、两次候选尝试，然后在脚本模拟回复后变为 `demo_reviewed`。这是**预期行为，不是本教程已获得的运行输出**。

限制：

- 需要安装并锁定与你使用的文档相匹配的 LangGraph 版本；本教程没有验证依赖组合或提供锁文件。
- 候选选择是程序预写的，不是模型修复代码。
- InMemorySaver 只展示同一进程内的状态；退出进程不能据此恢复。
- 回复由脚本模拟，未进行真实身份验证。
- 没有外部发布、通知或生产动作。

## OpenAI Agents SDK

[agents_collaboration.py](agents_collaboration.py) 对应第 18、19、22 课。

在自行准备兼容 SDK、模型和官方凭据配置后，可以选择工具式调用、handoff 或内存通知示意：

```bash
python -m framework_samples.agents_collaboration tools
python -m framework_samples.agents_collaboration handoff
python -m framework_samples.agents_collaboration notify
```

设置 `AGENT_MODEL` 为你账户可用的模型。不要把密钥写入文件或提交到 Git。运行将调用模型 API，可能产生费用；本教程未执行这些调用。

观察重点：

- `tools`：管理者可以调用审查者，返回后继续汇总。
- `handoff`：运行时可以切换当前 Agent，最后显示 active agent。
- `notify`：工具只向内存 outbox 追加事件，没有消费者，没有真实投递。

模型实际是否按预期调用工具，仍需要查看真实运行记录和测试。提示词不是调用保证，更不是权限强制。

## 你接下来可以怎样验证

先锁定 Python 与依赖版本，运行最小例子，记录实际输出与工具调用；再加入失败、拒绝和恢复测试。只有完成这些步骤，才能把“文档兼容的示意”升级为“这个依赖组合下验证过的示例”。
