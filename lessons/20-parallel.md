# 20 并行之后怎样可靠汇总

[上一课](19-handoff.md) · [学习路线](../README.md) · [下一课](21-triggers.md)

## 先问是否能独立工作

工单 1042 可以同时做两个只读任务：检查输入格式边界，检查已有测试覆盖。二者不必等待对方写代码。

两个 Agent 同时修改同一个函数则不同。它们可能覆盖彼此、基于不同版本工作，最后得到的组合也未必通过测试。并发启动容易，正确集成更难。

先并行只读任务，是降低学习难度的好起点。

## 动态派发怎样表达

LangGraph 的 `Send` 可以按当前状态派发多个任务。以下是未运行的片段：

```python
from langgraph.types import Send

def dispatch_reviews(state):
    return [
        Send("review_scope", {
            "head_sha": state["head_sha"],
            "scope": scope,
        })
        for scope in state["scope_checks"]
    ]
```

它不是完整图。`review_scope` 需要注册，派发函数需要接到条件边。上游可以由模型提出 `scope_checks`，但代码应先检查范围是否合法、数量和总预算是否可接受。[官方 Send 与 map reduce 指南](https://docs.langchain.com/oss/python/langgraph/use-graph-api#map-reduce-and-the-send-api)

## 多份结果放在哪里

如果每个分支都返回 `findings`，需要明确合并规则。例如：

```python
from typing import Annotated, TypedDict
import operator

class ReviewState(TypedDict):
    findings: Annotated[list[dict], operator.add]
```

这表示按列表相加来合并结果。它不会自动去重，也不会解决互相矛盾的意见。若分支可能重复执行，结果最好带稳定标识，再由汇总阶段按标识处理。

并行结果到达顺序也不应承担业务意义。需要稳定展示时，按明确字段排序，而不是把“先到”当成“更可信”。

## 汇总者必须做的检查

先核对结果属于同一个候选版本，再看每个任务是否完成、是否缺证据，最后处理冲突。一个 worker 失败不应让成功兄弟任务的结果消失，但也不能被整体成功掩盖。

可以报告“格式审查完成，回归覆盖审查超时，尚不足以批准交付”，而不是取已有结果凑一个成功结论。

## 读源码时别被图骗了

公开底盘里的 LLMCompiler 实现会计算依赖波次，但该版本同波节点的执行循环是串行。另一方面，受条件限制的 ReAct 批次有实际线程并行路径。DAG 看起来可以并行，与运行时真的并行，是两件事。[固定版本并行说明与源码](../references/sources.md#r04)

## 小练习

两个审查者分别支持“接受空字符串”和“拒绝空字符串”。汇总者该投票吗？先回到任务契约核对要求；缺少要求时提问，而不是靠多数票创造需求。

**带走一句话：并行的前提是可独立执行，汇总的前提是结果能对齐与验证。**
