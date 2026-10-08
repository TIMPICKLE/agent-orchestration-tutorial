# 图解索引

[学习路线](../README.md)

每张图只解释一个机制。建议打开对应课程，一起阅读图下的步骤、适用范围和来源；不要脱离正文把教学图当作某个产品的完整实现。所有图均为本地 SVG，按原始大小查看可放大文字。

## 建立任务与控制

- [先学会一个闭环，再增加能力](../README.md) · [查看图](../assets/diagrams/00-learning-map.svg)
- [把“修好”拆成四张可检查的卡](../lessons/01-task-and-done.md) · [查看图](../assets/diagrams/01-task-contract.svg)
- [谁决定下一步：两层控制](../lessons/02-control.md) · [查看图](../assets/diagrams/02-control-zones.svg)
- [一次工具请求怎样变成真实执行](../lessons/03-model-tool-agent.md) · [查看图](../assets/diagrams/03-tool-roundtrip.svg)
- [聊天、任务状态、产物各放哪里](../lessons/04-state.md) · [查看图](../assets/diagrams/04-state-shelves.svg)
- [失败后是否再尝试，是明确的设计选择](../lessons/05-python-workflow.md) · [查看图](../assets/diagrams/05-fixed-vs-feedback.svg)
- [一轮循环要带回什么](../lessons/06-agent-loop.md) · [查看图](../assets/diagrams/06-observation-loop.svg)
- [提示词之外，还要有执行门禁](../lessons/07-bounded-autonomy.md) · [查看图](../assets/diagrams/07-permission-gate.svg)
- [同样失败，下一步可能完全不同](../lessons/08-retry.md) · [查看图](../assets/diagrams/08-retry-triage.svg)

## 读源码与图运行时

- [外层生命周期与内层求解是两个选择](../lessons/09-repository-map.md) · [查看图](../assets/diagrams/09-two-control-axes.svg)
- [不要让外层重试重置整项任务预算](../lessons/10-chassis-flow.md) · [查看图](../assets/diagrams/10-nested-budgets.svg)
- [通过的是 A，为什么不能交付 B](../lessons/11-done-criteria.md) · [查看图](../assets/diagrams/11-evidence-binding.svg)
- [给自主会话一个可检查的外壳](../lessons/12-single-session.md) · [查看图](../assets/diagrams/12-session-envelope.svg)
- [节点、状态、边分别回答什么](../lessons/13-why-graph.md) · [查看图](../assets/diagrams/13-graph-vocabulary.svg)
- [沿着两个节点，看两个字段怎样更新](../lessons/14-first-langgraph.md) · [查看图](../assets/diagrams/14-state-updates.svg)
- [路由是有顺序的判断](../lessons/15-routing.md) · [查看图](../assets/diagrams/15-routing-table.svg)
- [等待可以跨执行，恢复必须找到同一状态](../lessons/16-persistence.md) · [查看图](../assets/diagrams/16-checkpoint-resume.svg)

## 协作与交付

- [专家作为工具：结果回到管理者](../lessons/18-manager-and-tools.md) · [查看图](../assets/diagrams/18-expert-call.svg)
- [返回结果、发消息、交接控制不要混用](../lessons/19-handoff.md) · [查看图](../assets/diagrams/19-handoff-compare.svg)
- [并行之后，先对齐再汇总](../lessons/20-parallel.md) · [查看图](../assets/diagrams/20-parallel-join.svg)
- [事件收到之后，还有三道不同的事实](../lessons/21-triggers.md) · [查看图](../assets/diagrams/21-event-run-result.svg)
- [发送成功、回复丢失：怎样避免盲目再发](../lessons/22-notifications.md) · [查看图](../assets/diagrams/22-outbox-uncertainty.svg)
- [批准要锁定人、动作、对象、版本](../lessons/23-human-approval.md) · [查看图](../assets/diagrams/23-approval-binding.svg)
- [谁提出任务，不等于用了谁的权限](../lessons/24-digital-employee.md) · [查看图](../assets/diagrams/24-four-identities.svg)
- [把交付链上的版本一段段连起来](../lessons/30-walkthrough.md) · [查看图](../assets/diagrams/30-evidence-chain.svg)

## 独立案例与场景选择

- [源码已有什么，还需要设计什么](../cases/01-chassis-judgment.md) · [查看图](../assets/diagrams/c01-fact-vs-design.svg)
- [保留会话自主性，补一个交付核验点](../cases/02-pure-agent-drive.md) · [查看图](../assets/diagrams/c02-session-verifier.svg)
- [主动做事与允许做事，是两个判断](../cases/03-meta-muse.md) · [查看图](../assets/diagrams/c03-muse-boundary.svg)
- [长期身份与任务，可以经历多次短运行](../cases/04-multica.md) · [查看图](../assets/diagrams/c04-multica-identities.svg)
- [执行触发与人类通知走不同路径](../cases/04-multica.md) · [查看图](../assets/diagrams/c04-mention-vs-inbox.svg)
- [任务保存在库里，实时通道只提示有活](../cases/05-multica-runtime.md) · [查看图](../assets/diagrams/c05-multica-wakeup.svg)
- [四种权限边界，要分别验证](../cases/06-multica-authority.md) · [查看图](../assets/diagrams/c06-authority-layers.svg)
- [三种任务，分别从最小有效方案开始](../design/scenario-decisions.md) · [查看图](../assets/diagrams/d01-scenario-choice.svg)

## Claude Code 专题

- [Claude Code：模型选择，运行支架落实](../cases/07-claude-code-runtime.md) · [查看图](../assets/diagrams/c07-claude-loop.svg)
- [四种扩展部件，各自改变什么](../cases/07-claude-code-runtime.md) · [查看图](../assets/diagrams/c07-extension-roles.svg)
- [恢复会话与定时启动，是两个能力](../cases/08-claude-code-collaboration.md) · [查看图](../assets/diagrams/c07-session-scheduling.svg)

先读图下的日期与适用范围。公开 SDK 的实现、厂商文档和独立重建是不同证据，详见[源码阅读案例](../cases/09-claude-code-source-reading.md)。

## 不需要每一课都加一张图

第 17 课关注增加角色的理由，第 25–29 课关注反例、评估与取舍，第 31–32 课用于自己设计和对照答案。这些课可复用前面的图进行检查，而不重复堆叠流程图。具体可用第 20 课检查协作，第 08、22、23 课设计故障，第 30 课检查证据关联，再回到设计工作表。
