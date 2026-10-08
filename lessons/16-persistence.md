# 16 暂停 保存与恢复

[上一课](15-routing.md) · [学习路线](../README.md) · [下一课](17-why-multi-agent.md)

## 等待不是一直占着一个函数

假设需要人确认补丁范围，人今天不在线。如果你的实现只是 `input()` 或一个进程内等待对象，进程退出后可能失去等待上下文。

更可靠的思路是：保存“我在等什么”，结束当前执行，收到有效回复后从相同任务继续。这样工作可以跨过进程重启和长时间等待。

## LangGraph 提供哪些部件

`checkpointer` 保存图的执行状态；`thread_id` 标识属于哪次连续运行；`interrupt()` 抛出等待人或外部输入的请求；`Command(resume=...)` 带着答案恢复。这里的 thread 是框架中的会话标识，不是操作系统线程。[持久化文档](https://docs.langchain.com/oss/python/langgraph/persistence)、[中断文档](https://docs.langchain.com/oss/python/langgraph/interrupts)

```python
from langgraph.types import interrupt, Command

def ask_scope(state):
    answer = interrupt({"question": "是否接受本次补丁范围？"})
    return {"scope_accepted": answer}

# graph 需先配置合适的 checkpointer。
config = {"configurable": {"thread_id": "demo-1042-run-1"}}
# 首次执行暂停后，由应用验证回复再恢复。
# graph.invoke(Command(resume=True), config=config)
```

这段是概念演示，不能把任意网络请求中的 `True` 直接传进来。真实服务要核对回复者、问题、目标版本和允许的决策。

[完整示例](../framework_samples/langgraph_complete.py) 包含 checkpointer 装配、第一次 invoke、检查暂停及第二次 resume。为控制学习成本，它使用内存 saver，只演示同一进程内暂停；不能作为跨重启示例。文件中的回复是脚本构造的模拟输入，不是真实用户授权。

## 内存保存不等于跨重启保存

如果使用内存 saver，退出进程后内存就没有了。学习时很好用，不能据此声称已具备崩溃恢复。跨重启要使用适合部署的持久存储，并验证恢复行为。[checkpointer 说明](https://docs.langchain.com/oss/python/langgraph/checkpointers)

## 恢复可能重新执行节点开头

如果你在 `interrupt()` 前发送通知，恢复进入这个节点时可能再发一次。一个简单改进是把通知作为单独可去重步骤，让审批节点只负责等待和处理决策。

即使把外部动作放到中断之后，任意时刻的崩溃仍可能造成重复。这正是第 08 课的发送窗口问题。checkpoint 能帮助记住运行位置，不能把第三方服务和你的状态存储自动变成一笔原子事务。

## 小练习

设计一个实验：暂停后退出整个进程，再启动并恢复。如果依赖内存对象才能继续，说明你验证的只是同进程暂停，不是持久恢复。

**带走一句话：可靠等待保存的是任务与请求，恢复时还必须重新检查权限和证据。**
