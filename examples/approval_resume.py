"""04: 保存/恢复状态；审批绑定工件版本、动作与目标。只模拟审批。"""
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory


def version_of(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def new_state(content):
    return {"task": "demo-1042", "content": content, "version": version_of(content),
            "action": "publish_review_draft", "target": "fake://review/demo-1042",
            "status": "waiting_approval", "approval": None}


def grant_simulated_approval(state):
    """真实系统必须由经认证的人类入口写入，而非允许模型调用此函数。"""
    state["approval"] = {key: state[key] for key in ("task", "version", "action", "target")}


def save_state(path, state):
    path = Path(path)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)  # 教学用原子替换；不是多写者/断电耐久方案。


def load_state(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class FakeReviewProvider:
    def __init__(self):
        self.drafts = {}  # 仅当前进程内存；不声称是持久化外部服务。

    def publish(self, key, content):
        self.drafts.setdefault(key, content)
        return "fake-draft-1"


def resume(state, provider):
    if version_of(state["content"]) != state["version"]:
        return "invalid_artifact_version"
    expected = {key: state[key] for key in ("task", "version", "action", "target")}
    if state["approval"] != expected:
        return "approval_required"
    key = json.dumps(expected, sort_keys=True)
    state["draft_id"] = provider.publish(key, state["content"])
    state["status"] = "published_simulated"
    return state["status"]


if __name__ == "__main__":
    with TemporaryDirectory() as directory:
        path = Path(directory) / "state.json"
        state, provider = new_state("validated parser v1"), FakeReviewProvider()
        save_state(path, state)
        state = load_state(path)
        print("before_approval=" + resume(state, provider))
        grant_simulated_approval(state)
        save_state(path, state)
        state = load_state(path)
        print("after_approval=" + resume(state, provider))
        state["content"] = "validated parser v2"
        state["version"] = version_of(state["content"])
        print("after_change=" + resume(state, provider))
        print(f"simulated_drafts={len(provider.drafts)}")
