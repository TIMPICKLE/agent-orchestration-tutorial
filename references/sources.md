# 来源与证据索引

[学习路线](../README.md)

核查日期：2026 年 10 月 8 日。官方在线文档可能持续变化；除明确固定的仓库提交外，这里不是某个 SDK 发行版的兼容性承诺。

正文的例子、学习顺序和工作表是教学设计。来源用于核对概念、公开 API 和可见实现，不能把设计建议反推为来源项目已经具备的功能。

## 官方概念与框架资料

<a id="s01"></a>
### S01 Workflow 与 Agent 的区分

Anthropic，[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)，2024-12-19。用于区分代码预定流程与模型动态选择行动，并支持先从简单可评估方案开始的思路。

<a id="s02"></a>
### S02 OpenAI Agents SDK 的协作方式

- [Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [Agents](https://openai.github.io/openai-agents-python/agents/)
- [Handoffs](https://openai.github.io/openai-agents-python/handoffs/)

用于第 18–19 课：专家作为工具返回，与切换当前 active agent 是不同控制关系。

<a id="s03"></a>
### S03 LangGraph 的状态与图

[Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)。用于节点、状态、边、字段 reducer，以及 TypedDict 形式的示意。

<a id="s04"></a>
### S04 LangGraph 持久化

- [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [Checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers)

用于区分图状态保存、thread 标识和持久存储。内存 saver 不支持进程退出后的恢复；checkpoint 不保证外部副作用恰好一次。

<a id="s05"></a>
### S05 LangGraph 暂停与恢复

[Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)。用于 `interrupt()`、`Command(resume=...)`、同一 thread 恢复，以及节点重入的注意事项。

<a id="s06"></a>
### S06 OpenAI Agents SDK 人工参与

[Human in the loop](https://openai.github.io/openai-agents-python/human_in_the_loop/)。用于工具审批与运行状态恢复的框架说明，不作为业务授权自动正确的证据。

<a id="s07"></a>
### S07 Deep Agents 的运行支架

- [Overview](https://docs.langchain.com/oss/python/deepagents/overview)
- [Subagents](https://docs.langchain.com/oss/python/deepagents/subagents)

用于解释文件、上下文、子 Agent 等 harness 能力。默认规划行为和配置继承会随版本变化，本文不依赖未锁定的默认值。

<a id="s08"></a>
### S08 Open SWE 应用参考

[langchain-ai/open-swe](https://github.com/langchain-ai/open-swe)。用于观察完整软件工程应用的职责组合。本教程未运行该系统，不把 README 的产品范围当成本教程验证过的功能。

<a id="s09"></a>
### S09 托管会话与环境

- Anthropic，[Managed Agents 工程说明](https://www.anthropic.com/engineering/managed-agents)，2026-04-08
- [Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)

用于 session log、harness、sandbox 的职责分离，以及托管基础设施与业务验收的区别。核查时该产品文档标记为 beta。

<a id="s10"></a>
### S10 多 Agent 的收益与代价

Anthropic，[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)，2025-06-13。用于并行探索、明确委派与上下文分离的经验参考；不将厂商单一系统的性能或成本观察泛化为保证。

<a id="s11"></a>
### S11 Agent 评估

Anthropic，[Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)，2026-01-09。用于区分对话记录与环境实际结果，并结合多种评分方式与多次试验。

<a id="s12"></a>
### S12 幂等与重试

Amazon Builders' Library，[Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)。用于区分同一请求的重试与新的意图，并说明外部结果不确定时的重复副作用风险。

<a id="s13"></a>
### S13 异步子任务

[Deep Agents async subagents](https://docs.langchain.com/oss/python/deepagents/async-subagents)。用于异步任务 ID 与 start/check/update/cancel/list 生命周期。需配套 Agent Protocol 服务；本文不从这些接口推断完成后自动唤醒主管。

<a id="s14"></a>
### S14 LangGraph 的路由与派发

[Use the Graph API](https://docs.langchain.com/oss/python/langgraph/use-graph-api)，特别是 [Send 与 map reduce](https://docs.langchain.com/oss/python/langgraph/use-graph-api#map-reduce-and-the-send-api)。用于条件边、动态分派与并行更新规则。

<a id="s15"></a>
### S15 工具注册与执行

[OpenAI Agents SDK tools](https://openai.github.io/openai-agents-python/tools/)。用于 `function_tool` 和运行上下文参数示例。示例中的 outbox 与消费者是教学应用自行定义，不是 SDK 自动提供的可靠消息总线。

<a id="s16"></a>
### S16 MCP 的职责

[What is MCP](https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro)。用于区分连接 AI 应用与外部系统的标准化能力，以及业务调度、权限和验收等应用职责。

## 公开底盘源码

以下均固定到公开仓库 `TIMPICKLE/devops-agent-chassis` 的提交 `63f8496eac20828f0712c8a53e2299a9b7baf8d8`。

<a id="r01"></a>
### R01 主运行器

[chassis.py](https://github.com/TIMPICKLE/devops-agent-chassis/blob/63f8496eac20828f0712c8a53e2299a9b7baf8d8/src/agent_chassis/chassis.py#L177-L336)。支撑任务获取、运行上下文、尝试、失败收尾，以及编排器宣称成功后的判据检查。

<a id="r02"></a>
### R02 运行上下文

[contracts.py](https://github.com/TIMPICKLE/devops-agent-chassis/blob/63f8496eac20828f0712c8a53e2299a9b7baf8d8/src/agent_chassis/contracts.py#L347-L458)。支撑事实、模型笔记、调用与验证记录的结构区分；这些字段不是防伪证明。

<a id="r03"></a>
### R03 权限检查的实际路径

- [PermissionBoundary](https://github.com/TIMPICKLE/devops-agent-chassis/blob/63f8496eac20828f0712c8a53e2299a9b7baf8d8/src/agent_chassis/permissions.py#L45-L128)
- [ToolBox](https://github.com/TIMPICKLE/devops-agent-chassis/blob/63f8496eac20828f0712c8a53e2299a9b7baf8d8/src/agent_chassis/orchestration/__init__.py#L119-L198)
- [显式检查的工具 wrapper](https://github.com/TIMPICKLE/devops-agent-chassis/blob/63f8496eac20828f0712c8a53e2299a9b7baf8d8/payloads/code_quality.py#L219-L246)

边界需要在执行路径中接线。不能从对象存在推断所有 shell、文件或连接器受到操作系统级隔离。

<a id="r04"></a>
### R04 推理与并行

- [ReAct 批次实现](https://github.com/TIMPICKLE/devops-agent-chassis/blob/63f8496eac20828f0712c8a53e2299a9b7baf8d8/src/agent_chassis/orchestration/reasoning.py#L190-L377)
- [LLMCompiler 波次实现](https://github.com/TIMPICKLE/devops-agent-chassis/blob/63f8496eac20828f0712c8a53e2299a9b7baf8d8/src/agent_chassis/orchestration/reasoning.py#L521-L590)
- [并行测试源码](https://github.com/TIMPICKLE/devops-agent-chassis/blob/63f8496eac20828f0712c8a53e2299a9b7baf8d8/tests/test_parallel_react.py)

用于区分图上可并行、执行器实际并发和远端服务并行。教程没有自行测量这些实现的性能。

<a id="r05"></a>
### R05 账本与失败处理

[failure.py](https://github.com/TIMPICKLE/devops-agent-chassis/blob/63f8496eac20828f0712c8a53e2299a9b7baf8d8/src/agent_chassis/failure.py)。默认账本是内存实现；路径模式使用 JSON 文件，不能据此推断事务、跨进程锁或断电恢复保证。补偿回调不等于所有远端影响都可撤销。

<a id="r06"></a>
### R06 人类回调

[orchestration 中的子图与人类回调](https://github.com/TIMPICKLE/devops-agent-chassis/blob/63f8496eac20828f0712c8a53e2299a9b7baf8d8/src/agent_chassis/orchestration/__init__.py#L420-L465)。当前可见同步回调不能当作持久审批、身份验证和产物绑定的完整实现。

<a id="r07"></a>
### R07 产物证据与配方

- [配置候选校验](https://github.com/TIMPICKLE/devops-agent-chassis/blob/63f8496eac20828f0712c8a53e2299a9b7baf8d8/payloads/config_policy.py#L45-L118)
- [配方实例化](https://github.com/TIMPICKLE/devops-agent-chassis/blob/63f8496eac20828f0712c8a53e2299a9b7baf8d8/employee_factory/recipes.py#L188-L273)
- [实例校验及运行](https://github.com/TIMPICKLE/devops-agent-chassis/blob/63f8496eac20828f0712c8a53e2299a9b7baf8d8/employee_factory/recipe_runtime.py#L15-L114)
- [生产证据边界文档](https://github.com/TIMPICKLE/devops-agent-chassis/blob/63f8496eac20828f0712c8a53e2299a9b7baf8d8/docs/PRODUCTION_EVIDENCE.md)

文件一致性、环境存在检查、真实外部运行和获准发布，分别是不同结论。

<a id="r08"></a>
### R08 查询到的公开 CI 状态

- [Digital Employee Acceptance run 35045781461](https://github.com/TIMPICKLE/devops-agent-chassis/actions/runs/35045781461)
- [Role Recipes run 35045781488](https://github.com/TIMPICKLE/devops-agent-chassis/actions/runs/35045781488)

研究时 API 显示上述提交的两个运行均为 completed/success。这是远端状态查询，非本地重跑；未据此确认确切测试数量，也不推导出真实 Azure、模型、发布权限或生产就绪状态。

<a id="r09"></a>
### R09 获准公开的 Pure Agent Drive 架构事实

来源仓库：`TIMPICKLE/AzureCodeAgent_Pure_Agent_Drive`。核对提交：`29909c544c74df7f5debff271ccb923ea24d9099`。作者已明确授权公开相关项目内容；研究时源仓库仍为私有，公众可能无法访问。教程只解释与场景有关的实现，不包含凭据、业务数据、内部地址或源码原文整段复制。

核对位置：

- `service.py`：任务消费、启动恢复和会话交接。
- `task_prompt.py` 中 `build_task_prompt()`：任务范围、自主推进与交付要求。
- `claude_runner.py` 中 `run()`、`build_command()`、`_valid_report()`：进程、超时和结果协议校验。
- `events.py`：事件身份。
- `task_store.py` 中 `enqueue()`、`claim()`、`reserve_execution()`、`recover()`：任务持久化、去重和恢复。

证据级别是固定版本源码阅读。未在本次研究中运行该服务，未调用真实模型、Azure 或研发工作流。独立交付核验与更强权限执行边界是教程建议，不是该版本已经实现的能力。

## 产品与公开实现

<a id="p03"></a>
### P03 Meta Muse

- [官方发布](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)
- [设计介绍](https://introducing.muse.ai/)
- [安全与权限工程说明](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)

这是具有明确厂商与来源的独立案例。产品体验来自厂商说明，底层能力来自公开工程描述，不是本教程实测或源码审计。

<a id="p04"></a>
### P04 mu 的 hive

固定提交 `537d028f483eae210f049a922e9c8e473a1b005d`。

- [board.ts](https://github.com/qybaihe/mu/blob/537d028f483eae210f049a922e9c8e473a1b005d/packages/kyrn-judge/src/hive/board.ts)
- [hive.ts](https://github.com/qybaihe/mu/blob/537d028f483eae210f049a922e9c8e473a1b005d/packages/kyrn-judge/src/extension/features/hive.ts)

用于研究发现、争议、更正与按接收者筛选的共享知识。文件日志与相关性模型不自动提供分布式一致性或漏发保证。

<a id="p05"></a>
### P05 Multica 的身份 任务与触发

官方仓库：[multica-ai/multica](https://github.com/multica-ai/multica)。固定提交 `8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec`。

- [Agents](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/apps/docs/content/docs/agents.mdx)
- [Runs](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/apps/docs/content/docs/tasks.mdx)
- [Triggering](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/apps/docs/content/docs/triggering-agents.mdx)
- [Inbox](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/apps/docs/content/docs/inbox.mdx)
- [入口触发实现](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/server/internal/service/issue_trigger.go)

支撑 Agent 与 Run 的区分、任务与评论触发，以及人类 inbox 不等同 Agent 执行队列。

<a id="p06"></a>
### P06 Multica 的协作与可靠唤醒

- [Squad briefing](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/server/internal/handler/squad_briefing.go#L32-L168)
- [实时通知](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/server/internal/daemonws/notifier.go)
- [daemon 唤醒](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/server/internal/daemon/wakeup.go)
- [任务领取与状态 SQL](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/server/pkg/db/queries/agent.sql#L749-L1000)
- [FinalizeTaskClaim](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/server/internal/service/task.go#L3799-L3867)
- [Issue Wakeup](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/server/internal/service/issue_wakeup.go)
- [Wakeup 条件](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/server/internal/service/issue_wakeup_condition.go)
- [Wakeup 输入合并](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/server/internal/service/issue_wakeup_join.go)

Squad 的生成协议与后端强制约束应分开解释。数据库竞争控制与通知 fallback 不构成所有外部动作恰好一次的保证。

<a id="p07"></a>
### P07 Multica 的身份与权限

- [Agent 调用权限](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/server/internal/service/agent_invocation.go)
- [授权来源与问责归属](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/server/internal/attribution/attribution.go)
- [owner 应用连接筛选](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/server/internal/integrations/composio/dispatch.go#L55-L125)
- [安全模型](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/apps/docs/content/docs/security-model.mdx)

用于区分启动 Agent、平台 API、宿主系统及外部服务四类权限。教程不宣称默认执行环境适合所有多人风险场景。

<a id="p08"></a>
### P08 Multica 的上下文与许可

- [prompt 装配](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/server/internal/daemon/prompt.go)
- [原生记忆处理](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/server/internal/daemon/execenv/codex_memory.go)
- [Skills](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/apps/docs/content/docs/skills.mdx)
- [LICENSE](https://github.com/multica-ai/multica/blob/8db6cfe19ae6fd5c35ec71bd8fea42a3ef3861ec/LICENSE)

用于说明显式上下文与跨任务记忆的边界。阅读设计不等于获得任意复用全部产品代码的许可。

<a id="p09"></a>
### P09 Claude Code：公开文档、组件源码与分析资源

核对日期为 **2026 年 10 月 8 日**。下面的官方文档与 `main` 分支会继续变化；涉及子代理、团队、权限模式和定时功能时，应核对自己的版本与运行方式。此次没有运行 Claude Code、调用模型或执行第三方示例。

**官方行为说明：**

- [运行原理与上下文](https://code.claude.com/docs/en/how-claude-code-works)
- [扩展部件分工](https://code.claude.com/docs/en/features-overview)
- [子代理](https://code.claude.com/docs/en/sub-agents) · [实验性 Agent teams](https://code.claude.com/docs/en/agent-teams) · [跨会话消息](https://code.claude.com/docs/en/cross-session-messaging)
- [权限](https://code.claude.com/docs/en/permissions) · [沙箱](https://code.claude.com/docs/en/sandboxing)
- [会话管理](https://code.claude.com/docs/en/sessions) · [定时任务](https://code.claude.com/docs/en/scheduled-tasks) · [动态工作流](https://code.claude.com/docs/en/workflows)

**可读的官方组件：**

- [Python Agent SDK 源码](https://github.com/anthropics/claude-agent-sdk-python/tree/f7b0b62c2a8d110d4da0eec0aa70cf795ec3afc4/src/claude_agent_sdk)，重点读 [CLI 子进程传输](https://github.com/anthropics/claude-agent-sdk-python/blob/f7b0b62c2a8d110d4da0eec0aa70cf795ec3afc4/src/claude_agent_sdk/_internal/transport/subprocess_cli.py) 和 [请求与控制协议](https://github.com/anthropics/claude-agent-sdk-python/blob/f7b0b62c2a8d110d4da0eec0aa70cf795ec3afc4/src/claude_agent_sdk/_internal/query.py)。这里固定到提交 `f7b0b62c2a8d110d4da0eec0aa70cf795ec3afc4`。它们说明 SDK 与 CLI 的边界，不能证明闭源核心的全部调度实现。
- [Sandbox Runtime](https://github.com/anthropics/sandbox-runtime/tree/3f0bad7345238f47736435e3f2b064399c1cad74)：官方开放组件，用于研究执行隔离；不是整个 Claude Code 的源码。
- [Agent SDK 应用示例](https://github.com/anthropics/claude-agent-sdk-demos)：用于理解外围应用设计，不是 CLI 内部实现。

[Claude Code 产品仓库](https://github.com/anthropics/claude-code) 的公开可见性不代表核心运行时以开源许可发布；应分别查看 [产品仓库许可](https://github.com/anthropics/claude-code/blob/main/LICENSE.md) 与 [Python SDK 许可](https://github.com/anthropics/claude-agent-sdk-python/blob/main/LICENSE)。独立分析和教学重建不能作为官方当前实现的直接证据。

完整资源分级与阅读顺序见 [Claude Code 源码与分析阅读指南](claude-code-reading.md)；案例见 [运行循环](../cases/07-claude-code-runtime.md)、[协作与持续运行](../cases/08-claude-code-collaboration.md)、[怎样读源码分析](../cases/09-claude-code-source-reading.md)。


<a id="p10"></a>
### P10 Claude Code 历史源码与版本证据

[历史源码阅读索引](claude-code-historical-reading.md)列出五个候选的固定提交、来源类型与版本局限；其中实际精读的 2.1.88 快照来自 [ChinaSiro/claude-code-sourcemap](https://github.com/ChinaSiro/claude-code-sourcemap/tree/a8a678cb6244e6770e1e421767ff0987a1d95549)。核心阅读入口是 `query.ts`、`toolOrchestration.ts`、`StreamingToolExecutor.ts`、`toolExecution.ts`、`runAgent.ts` 和 `autoCompact.ts`，逐项链接在索引与[案例十](../cases/10-historical-query-loop.md)至[案例十二](../cases/12-historical-subagent-context.md)。

包元数据与提取脚本支持仓库自述，但不等于官方签名认证或开源许可。内容是静态阅读及原创分析，未运行历史产品，也不据旧代码推断当前版本行为。
