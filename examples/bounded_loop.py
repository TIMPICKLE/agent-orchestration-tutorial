"""02: 有预算的反馈循环。ScriptedFakeModel 只是脚本，不是 LLM。"""
from dataclasses import dataclass
from .fixed_workflow import original, tempting_fix, parse_amount, acceptance_failures


@dataclass(frozen=True)
class Action:
    tool: str
    candidate: str = ""


class ScriptedFakeModel:
    """预设输出方便重现实验；不体现真实模型推理能力。"""
    def __init__(self, actions):
        self.actions = iter(actions)
        self.observations = []

    def decide(self, observation):
        self.observations.append(observation)
        return next(self.actions, Action("finish"))


CANDIDATES = {"original": original, "strip_commas": tempting_fix, "validated": parse_amount}


def run_agent(model, max_steps=5):
    candidate = "original"
    tested_candidate = None
    passed = False
    trace = []
    observation = {"task": "demo-1042", "status": "start"}
    for step in range(max_steps):
        action = model.decide(observation)
        # 模型只提出动作；宿主负责白名单、预算和完成判断。
        if not isinstance(action, Action):
            return {"status": "invalid_action", "steps": step + 1, "trace": trace}
        if action.tool == "select_patch" and action.candidate in CANDIDATES:
            candidate = action.candidate
            tested_candidate, passed = None, False  # 新候选必须重测。
            observation = {"selected": candidate}
        elif action.tool == "test":
            failures = acceptance_failures(CANDIDATES[candidate])
            tested_candidate, passed = candidate, not failures
            observation = {"candidate": candidate, "failures": failures}
        elif action.tool == "finish":
            status = "ready_for_review" if passed and tested_candidate == candidate else "unverified_finish"
            return {"status": status, "steps": step + 1, "trace": trace}
        else:
            return {"status": "denied_action", "steps": step + 1, "trace": trace}
        trace.append(observation)
    return {"status": "budget_exhausted", "steps": max_steps, "trace": trace}


def demo_model():
    return ScriptedFakeModel([Action("select_patch", "strip_commas"), Action("test"),
                              Action("select_patch", "validated"), Action("test"), Action("finish")])


if __name__ == "__main__":
    result = run_agent(demo_model())
    print("model=ScriptedFakeModel (offline, not an LLM)")
    print(f"first_test_failed={bool(result['trace'][1]['failures'])}")
    print(f"status={result['status']}; steps={result['steps']}")
    print("budget_demo=" + run_agent(demo_model(), max_steps=2)["status"])
