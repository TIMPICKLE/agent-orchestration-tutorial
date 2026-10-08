"""完整装配示意，不是已运行验证的 LangGraph 集成。

需要单独安装并锁定兼容 LangGraph 版本；本文件不调用模型、不联网、不发布。
候选实现预先写好，测试来自离线示例。InMemorySaver 只演示同进程暂停。
API reference: https://docs.langchain.com/oss/python/langgraph/interrupts
"""
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from examples.fixed_workflow import acceptance_failures, parse_amount, tempting_fix


class State(TypedDict):
    task_id: str
    candidate_key: str
    attempt: int
    failures: list[str]
    status: str


CANDIDATES = {"strip_commas": tempting_fix, "validated": parse_amount}


def propose(state: State):
    # 预写选择顺序，演示控制流；没有模型生成或自适应修复。
    key = "strip_commas" if state["attempt"] == 0 else "validated"
    return {"candidate_key": key, "attempt": state["attempt"] + 1,
            "failures": [], "status": "testing"}


def verify(state: State):
    failures = acceptance_failures(CANDIDATES[state["candidate_key"]])
    return {"failures": failures,
            "status": "needs_repair" if failures else "waiting_for_review"}


def after_verify(state: State):
    if not state["failures"]:
        return "request_review"
    if state["attempt"] < 2:
        return "propose"
    return "blocked"


def request_review(state: State):
    # 中断前没有发送消息或执行其他外部写入。
    reply = interrupt({
        "task_id": state["task_id"],
        "candidate_key": state["candidate_key"],
        "question": "教学演示中，是否把这份候选标记为已审阅？",
    })
    # 只验证模拟字段，不构成真实身份认证或发布授权。
    valid = (
        isinstance(reply, dict)
        and reply.get("task_id") == state["task_id"]
        and reply.get("candidate_key") == state["candidate_key"]
        and reply.get("accepted") is True
    )
    return {"status": "demo_reviewed" if valid else "demo_rejected"}


def report(state: State):
    # 保留 request_review 的结论；无发送或发布副作用。
    return {"status": state["status"]}


def blocked(state: State):
    return {"status": "blocked"}


def build_graph():
    builder = StateGraph(State)
    builder.add_node("propose", propose)
    builder.add_node("verify", verify)
    builder.add_node("request_review", request_review)
    builder.add_node("report", report)
    builder.add_node("blocked", blocked)
    builder.add_edge(START, "propose")
    builder.add_edge("propose", "verify")
    builder.add_conditional_edges("verify", after_verify, {
        "request_review": "request_review", "propose": "propose",
        "blocked": "blocked",
    })
    builder.add_edge("request_review", "report")
    builder.add_edge("report", END)
    builder.add_edge("blocked", END)
    return builder.compile(checkpointer=InMemorySaver())


def main():
    graph = build_graph()
    config = {"configurable": {"thread_id": "demo-1042-langgraph-run-1"}}
    initial: State = {
        "task_id": "demo-1042", "candidate_key": "", "attempt": 0,
        "failures": [], "status": "ready",
    }
    graph.invoke(initial, config=config)
    snapshot = graph.get_state(config)
    print("Before simulated reply:", snapshot.values["status"])
    print("Attempts:", snapshot.values["attempt"])
    print("Next node:", snapshot.next)
    # 这里故意自动构造模拟答案，便于展示 resume 语法。
    # 真实应用必须由已认证入口核验正式请求和批准范围。
    reply = {"task_id": "demo-1042", "candidate_key": "validated", "accepted": True}
    final = graph.invoke(Command(resume=reply), config=config)
    print("After simulated reply:", final["status"])


if __name__ == "__main__":
    main()
