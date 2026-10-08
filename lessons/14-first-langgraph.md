# 14 读懂你的第一张 StateGraph

[上一课](13-why-graph.md) · [学习路线](../README.md) · [下一课](15-routing.md)

## 先看没有模型的图

下面按官方公开接口写一个最小教学片段。它展示图的形状，未在本教程中安装对应依赖运行；以 [验证记录](../references/verification.md) 为准。它使用固定测试结果，不是实际修复或测试。

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    issue: str
    candidate: str
    passed: bool

def propose(state: State):
    return {"candidate": "strip thousands separator"}

def verify(state: State):
    return {"passed": state["candidate"] == "strip thousands separator"}

builder = StateGraph(State)
builder.add_node("propose", propose)
builder.add_node("verify", verify)
builder.add_edge(START, "propose")
builder.add_edge("propose", "verify")
builder.add_edge("verify", END)
graph = builder.compile()

result = graph.invoke({"issue": "demo-1042", "candidate": "", "passed": False})
```

接口依据：[Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)。这段相等判断只证明玩具状态流转；不能用来证明真实解析函数正确。

想看节点、路由、初始状态和暂停恢复装在一起的完整文件，可以在读完第 16 课后看 [完整 LangGraph 示例](../framework_samples/langgraph_complete.py)；它使用真实本地测试函数与预先写好的候选，不调用模型。框架集成尚未运行。

## 按四块来读

第一块是 `State`。它告诉读者状态有哪些字段。`TypedDict` 帮助声明预期结构，但不会自动验证每个来自外部的值。真实入口还需进行数据校验。

第二块是节点函数。`propose` 只返回要更新的 `candidate`；`verify` 只返回 `passed`。它们不必把全部状态复制一遍。

第三块是装配。`add_node` 登记可以运行的函数；`add_edge` 规定顺序。节点的显示名称和函数本身是两个概念，但可以用同样的词降低理解负担。

第四块是运行。`compile()` 生成可执行图；`invoke()` 传入初始状态并开始执行。

## 为什么没有模型也值得学

这样做可以把两个问题分开：图是否按预期运行，以及模型是否提出了好方案。两个问题同时出错时，很难定位。

当这个结构清楚后，你可以替换 `propose` 的内部，让它调用模型或完整修复 Agent。图的外部顺序无需因此改变。

## 状态更新怎样合并

单一路径中，普通字段的新值可以替换旧值。如果多条并行路径同时给同一字段结果，就需要明确合并规则，LangGraph 用 reducer 表达这种规则。

先记住需求即可：多个结果放到一起时，必须说明是覆盖、追加还是按标识合并。第 20 课再写 reducer。

## 小练习

把 `verify` 改成固定返回 `False`，按照现在的边，流程会到哪里？答案是仍然结束。下一课给它真正的失败路由。

**带走一句话：StateGraph 把状态 节点和连接关系分别写清楚。**
