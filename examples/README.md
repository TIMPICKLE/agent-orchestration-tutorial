# 四个可以离线跑的小实验

先看控制流，再接模型。这里所有模型、工单、审批和外部服务都是教学模拟，工单编号为 `demo-1042`。没有 API key，不安装依赖，不连接 Azure DevOps/GitHub，不创建真实 PR，也不发真实通知。

## 准备：只需要 Python

使用 Python 3.10 或更新版本。实际验证版本为 Python 3.12.14，其他版本未逐一验证。打开终端，进入仓库根目录（能看到 `examples/` 和 `tests/` 的位置），运行：

```bash
python --version
python -m unittest discover -s tests -v
```

部分电脑需要把 `python` 换成 `python3`。测试最后应显示 `Ran 24 tests` 和 `OK`；运行时间会变化。不要进入 `examples/` 后直接运行文件，下面使用的是包运行方式。

金额输入的约定：只接受非负 ASCII 数字。整数可以不带逗号，或使用正确的三位千位分组；小数点后如有小数，必须恰好两位。不接受正负号、空格、货币符号、指数、特殊值或其他地区的金额写法。无逗号的 `0012` 可接受，有逗号的 `01,234` 不接受。这只是本练习的业务约定，并非所有产品的规则。返回 `Decimal`，避免浮点数金额误差。

## 实验一：先把固定流程跑通

阅读 [fixed_workflow.py](fixed_workflow.py)，然后运行：

```bash
python -m examples.fixed_workflow
```

预期输出：

```text
demo-1042: initial_failed=True
tests_passed=True; status=ready_for_review
tempting_fix rejected by regression suite=True
```

分三步看：

1. `original` 使用 `Decimal(text)`，遇到千位逗号会失败。这里从头到尾用 Decimal 保持金额精确。
2. `tempting_fix` 去掉所有逗号，能通过工单里的单个例子，却也接受错误的 `12,34.50`。
3. `parse_amount` 先验证语法再去逗号，必须通过目标测试和回归测试，才得到 `ready_for_review`。

此时没有 Agent。程序预先决定全部步骤，补丁也由作者预先写好。

小练习：给 `acceptance_failures` 增加 `"1,23,456.00"` 的拒绝断言，然后重跑测试。为什么只有目标输入通过还不算完成？

## 实验二：让下一步来自一个受约束的选择器

阅读 [bounded_loop.py](bounded_loop.py)，运行：

```bash
python -m examples.bounded_loop
```

预期输出：

```text
model=ScriptedFakeModel (offline, not an LLM)
first_test_failed=True
status=ready_for_review; steps=5
budget_demo=budget_exhausted
```

从 `demo_model()` 看五个动作：选择宽松补丁 → 测试失败 → 选择校验补丁 → 测试通过 → 请求结束。

- `ScriptedFakeModel` 按脚本输出动作，并记录收到的观察结果。它没有推理能力，不会根据测试动态生成补丁。
- `run_agent` 是宿主循环：负责允许哪些动作、每次动作消耗一步预算，以及什么证据才允许结束。
- 模型请求 `finish` 不代表任务完成。没有当前候选的通过记录，就返回 `unverified_finish`。
- 改了候选实现，旧测试证据立刻失效。预算用完就停止，不无限重试。

小练习：把脚本第一步改为 `Action("finish")`。猜结果，再通过测试或交互式 Python 验证。再把 `max_steps` 改成 2，观察系统停在哪里。

## 实验三：最麻烦的超时，发生在成功之后

阅读 [message_delivery.py](message_delivery.py)，运行：

```bash
python -m examples.message_delivery
```

预期输出：

```text
first_event=True
duplicate_event=False
first_attempt=unknown
after_reopen=reconciled
external_effects=1
```

只追踪一个事件：

1. `receive` 在同一 SQLite 事务内记下 inbox 事件和待发送 outbox；相同事件 ID 不重复产生动作。
2. 模拟外部服务先把副作用写入自己的数据库，再故意丢掉响应。宿主只能说 `unknown`。
3. 关闭并重新打开本地数据库连接，使用同一个幂等键向模拟服务查询。找到相同内容，标记 `reconciled`，不重复发送。

两个数据库都在自动清理的临时目录内。`FakeProvider` 只是用第二个 SQLite 文件模拟独立系统。测试还关闭、重开两边连接，检查数据仍在；没有真正杀进程或断网。

重要边界：这个示例只演示单写者、顺序消费；inbox/outbox 不是并发 worker 实现。示例依赖服务端支持幂等键、可靠查询和内容比对。它不是适用于任何 API 的“恰好一次”保证。服务不支持这些能力时，需要业务唯一标识、人工对账或其他恢复策略。多 worker 领取任务、租约、退避、认证、保留期均未实现。

小练习：同一个事件 ID 换成不同正文。为什么应该报冲突，而不是静默当成重复消息？

## 实验四：审批不能跟着旧版本漂移

阅读 [approval_resume.py](approval_resume.py)，运行：

```bash
python -m examples.approval_resume
```

预期输出：

```text
before_approval=approval_required
after_approval=published_simulated
after_change=approval_required
simulated_drafts=1
```

1. 保存 JSON 状态，再重新加载。没有审批时不产生副作用。
2. `grant_simulated_approval` 模拟人确认当前版本，绑定任务、内容哈希、动作和目标。
3. 内容改成 v2，即使旧审批还在，宿主也要求重新批准。目标或动作改变，同样失效。

这不是安全认证系统。真实审批必须来自经验证的人类身份，不能暴露为模型可调用的自批工具。JSON 原子替换也不提供多写者控制、审计防篡改或断电耐久保证。模拟发布结果只在当前进程的内存中；持久化副作用和对账请对照实验三，不能仅凭这里的内存字典推断崩溃恢复安全。

小练习：只改 `target`，不改内容。为什么还应该重新审批？

## 哪些内容真的测过

[VERIFICATION.md](VERIFICATION.md) 记录实际命令、测试范围和未验证边界。自动化断言位于 [tests/test_examples.py](../tests/test_examples.py)。这些示例说明控制流和失败处理，不代表真实 LLM、SDK、网络、授权或生产环境已通过验证。
