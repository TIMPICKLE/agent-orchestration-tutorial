"""OpenAI Agents SDK 原创接口示意，未执行模型或框架集成测试。

若自行运行，本文件会调用所配置的模型 API，可能产生费用。
只处理虚构数据；没有仓库写入、PR、部署或对外消息工具。
References: https://openai.github.io/openai-agents-python/multi_agent/
            https://openai.github.io/openai-agents-python/tools/
"""
import argparse
import asyncio
import os
from dataclasses import dataclass, field

from agents import Agent, RunContextWrapper, Runner, function_tool, handoff


@dataclass
class DemoContext:
    task_id: str
    # 内存待发箱，既不持久，也没有自动消费者。
    outbox: list[dict] = field(default_factory=list)


@function_tool
async def notify_coordinator(ctx: RunContextWrapper[DemoContext], summary: str) -> str:
    """把教学任务的重要更新排入固定主管的内存待发箱。"""
    ctx.context.outbox.append({"task_id": ctx.context.task_id,
                               "kind": "worker_update", "summary": summary})
    return "queued in demo memory only; not delivered"


async def run_tools(model: str):
    reviewer = Agent(
        name="Patch reviewer", model=model,
        instructions="依据给定代码检查格式风险，指出缺失证据；不能声称执行过代码或测试。",
    )
    manager = Agent(
        name="Fix coordinator", model=model,
        instructions="负责整体结论。调用 review_patch 获取审查意见，再解释证据与限制。",
        tools=[reviewer.as_tool(
            tool_name="review_patch",
            tool_description="检查给定补丁是否放宽输入格式，返回证据和风险，不接管对话。",
        )],
    )
    result = await Runner.run(manager, (
        "虚构任务 demo-1042：金额仅允许合法千分位。补丁先删除所有逗号，再调用 Decimal。"
        "请调用审查工具检查非法输入 12,34.50 的风险。没有提供任何运行日志。"
    ))
    print(result.final_output)


async def run_handoff(model: str):
    acceptance = Agent(
        name="Acceptance assistant", model=model,
        instructions="接手解释如何确认输入格式需求，只讨论虚构任务，不代替用户批准发布。",
    )
    triage = Agent(
        name="Engineering triage", model=model,
        instructions="用户需要澄清验收步骤时，交接给 Acceptance assistant。",
        handoffs=[handoff(acceptance)],
    )
    result = await Runner.run(triage, "请交给验收助手，帮我梳理金额格式的验收问题。")
    print(result.final_output)
    print("Final active agent:", result.last_agent.name)


async def run_notify(model: str):
    context = DemoContext(task_id="demo-1042")
    worker = Agent(
        name="Investigator", model=model,
        instructions="只在虚构教学场景报告给出的发现，调用 notify_coordinator 排队更新。",
        tools=[notify_coordinator],
    )
    result = await Runner.run(worker, (
        "教学假设：当前验收材料缺少非法千分位规则。请把这一阻塞排入主管待发箱。"
        "不要宣称真的查过仓库或已经向人发送消息。"
    ), context=context)
    print(result.final_output)
    print("In-memory outbox:", context.outbox)
    print("No consumer exists; nothing has been delivered to a person.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["tools", "handoff", "notify"])
    args = parser.parse_args()
    model = os.environ.get("AGENT_MODEL")
    if not model:
        raise SystemExit("Set AGENT_MODEL to a model available to your account; do not commit credentials.")
    action = {"tools": run_tools, "handoff": run_handoff, "notify": run_notify}[args.mode]
    asyncio.run(action(model))


if __name__ == "__main__":
    main()
