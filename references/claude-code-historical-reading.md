# Claude Code 历史源码：来源、路线与自测

[案例十：主循环](../cases/10-historical-query-loop.md) · [案例十一：工具调度](../cases/11-historical-tool-scheduling.md) · [案例十二：子代理上下文](../cases/12-historical-subagent-context.md) · [官方组件与当前文档](claude-code-reading.md)

核对日期：**2026-10-08**。本轮实际静态阅读了社区历史快照中的实现文件，不只阅读 README 或 SDK。未安装、构建、运行或复制发布第三方源码；教程中的解释、伪代码和图均为原创。

## 怎样理解证据

- **源码观察**：在固定提交中确实存在的函数、条件和数据流
- **作者解释**：根据这些代码推导的设计意义，不等于官方设计意图
- **尚未验证**：官方产物字节一致性、运行时效果、线上开关是否启用、当前版本是否相同

社区公开保存的文件、可读源码、官方开源授权是三件事。选择可检验的快照，并不赋予它官方身份。

## 主读本：2.1.88 的来源链

[ChinaSiro/claude-code-sourcemap](https://github.com/ChinaSiro/claude-code-sourcemap/tree/a8a678cb6244e6770e1e421767ff0987a1d95549)，固定提交：

`a8a678cb6244e6770e1e421767ff0987a1d95549`

来源支持不止一个 README：

1. [说明](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/README.md) 明确自称非官方、从 npm 包的 source map 提取，版本 2.1.88。
2. 随仓 [package/package.json](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/package/package.json) 的包名为 `@anthropic-ai/claude-code`，版本为 2.1.88。
3. 树中保存 cli.js、cli.js.map 和 [extract-sources.js](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/extract-sources.js)。实际读到提取脚本按 sources 与 sourcesContent 对应内容写文件，而非要求模型重新发明实现。

这构成仓库内部可检查的来源链；本次没有下载完整 source map 或与官方 npm tarball 独立比对哈希，**不能称为完成官方真实性认证**。目录中有功能分支，也不能自动证明这些功能都曾对外开放。

## 五类候选，不要混成一种“源码”

### 1. source-map 提取快照：主读本

上述 ChinaSiro 仓库，固定 `a8a678cb6244e6770e1e421767ff0987a1d95549`，宣称版本 **2.1.88**。已经实际阅读主循环、工具调度与执行、子代理、自动压缩。

### 2. 更早的提取快照：仅作已读历史对照

[lyconear/Claude-Code 的固定提交](https://github.com/lyconear/Claude-Code/tree/da716d77b251868918bb5776377f85a18a47ffdf) 为 `da716d77b251868918bb5776377f85a18a47ffdf`，保存 2025-02-27 的提交历史，README 声称 **0.2.8 with extracted source maps**。已读 query、AgentTool、permissions、compact 等文件；没有核验原始 npm 产物的哈希。

研究时原 dnakov 仓库返回 **451 / DMCA**，不把它列为可用下载入口，也不尝试绕过。上面的独立公开候选是在获知该限制前找到并读取的；这里只保留已读机制的历史比较，不提供源码归档或再分发。

### 3. 标称反混淆，但版本证据冲突

[nadonghuang/claude-code](https://github.com/nadonghuang/claude-code/tree/d0a2351636cf80e0e8fb35efd9cb47941ddc76ff)，固定 `d0a2351636cf80e0e8fb35efd9cb47941ddc76ff`，README 声称 **2.1.76**、恢复名字/注释/类型，并列出缺失文件。

然而两仓 Git tree 返回：

- nadonghuang 的 src/query.ts 与 ChinaSiro 的 restored-src/src/query.ts，blob SHA 都为 `07e8b6fae53877a912424c0cdbbf321186eeca5f`
- 两份 QueryEngine.ts，blob SHA 都为 `0a80c6139b91551d105092016b9f8ce3240d37b0`

这证明所比文件内容一致，不证明两仓全部一致，也不单独决定哪个版本标签正确。不能用它们当作两份独立版本证据，再编造“2.1.76 到 2.1.88 的变化”。

### 4. Cleanroom 重构，不是原始实现证明

[ghuntley/claude-code-source-code-deobfuscation](https://github.com/ghuntley/claude-code-source-code-deobfuscation/tree/ced7586d06751d071490f91cab1de04490d969ba)，固定 `ced7586d06751d071490f91cab1de04490d969ba`，2025-03-01。

README 明说是 LLM cleanroom；项目自己 package.json 的 **0.1.0** 是重构项目版本，不能当作官方 Claude Code 对应版本。适合研究重构方法，不拿来证明原产品具体函数。

### 5. 教学实现与解析，适合对照练习

[shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code/tree/ce8f9f186058939da54c9d6fead78dfb5d0fd6c3)，固定 `ce8f9f186058939da54c9d6fead78dfb5d0fd6c3`。当前 README 区分 17 课主线和旧 12 课路线；它教你搭建类似 harness，没有一个可据此认定的官方 Claude Code 版本。

历史 analysis_claude_code 地址已发生跳转，不能将今天的教学树当作当年的 1.0.33 分析工作区。原创解析可帮助提问，具体实现结论仍回到固定代码核验。

## 精确阅读顺序：每次只追一个问题

以下均指主读本固定提交：

1. [query / queryLoop](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/restored-src/src/query.ts#L219-L307)：外层包装与状态循环怎样分工？
2. [deps](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/restored-src/src/query/deps.ts#L22-L38) → [模型调用](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/restored-src/src/query.ts#L655-L707)：实际调用谁，传入哪些状态？
3. [tool_use 收集](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/restored-src/src/query.ts#L826-L861) → [结果排空](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/restored-src/src/query.ts#L1380-L1408) → [下一份 State](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/restored-src/src/query.ts#L1705-L1728)：观察怎样进入下一轮？
4. [partitionToolCalls](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/restored-src/src/services/tools/toolOrchestration.ts#L19-L115) → [流式队列](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/restored-src/src/services/tools/StreamingToolExecutor.ts#L104-L150)：两种调度路径的屏障在哪里？
5. [执行检查入口](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/restored-src/src/services/tools/toolExecution.ts#L599-L635) → [权限判断](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/restored-src/src/services/tools/toolExecution.ts#L916-L1037) → [实际调用](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/restored-src/src/services/tools/toolExecution.ts#L1181-L1220)：动作请求何时变成效果？
6. [runAgent 初始消息](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/restored-src/src/tools/AgentTool/runAgent.ts#L368-L378) → [复用 query](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/restored-src/src/tools/AgentTool/runAgent.ts#L697-L757) → [结果映射](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/restored-src/src/tools/AgentTool/AgentTool.tsx#L1327-L1373)：子任务怎样进出？
7. [autoCompactIfNeeded](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/restored-src/src/services/compact/autoCompact.ts#L241-L349) → [超限恢复](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/restored-src/src/query.ts#L1062-L1182) → [Stop hooks](https://github.com/ChinaSiro/claude-code-sourcemap/blob/a8a678cb6244e6770e1e421767ff0987a1d95549/restored-src/src/query.ts#L1262-L1305)：局部恢复失败何时才变成全局终止？

看注释时再多做一步：调度注释用了 read-only，但实际分支调用的是带输入的 isConcurrencySafe。名称、注释、执行条件有差别时，以实际控制流为观察依据；不要把合理意图直接当成已验证效果。

## 六个源码问题与答案

### 1. 没有 tool_use，就一定完成吗？

不一定。2.1.88 的无工具路径还可能恢复上下文错误、处理阻塞 Stop hook，或进入受开关控制的继续分支。找 Terminal 返回点，而不是仅看一轮模型输出。

### 2. 并发安全 A、B，非安全 C，再安全 D，怎样排？

非流式路径将 A/B 合为并发批，C 单独串行，之后 D。是否安全来自解析后的输入与工具分类，异常时保守为不安全。这不是自动发现全任务依赖图。

### 3. C 权限被拒，会调用 tool.call 吗？

所读拒绝分支产生带 tool_use_id 的错误结果，不执行实际调用。调度器处理一个调用与该调用产生外部效果，是两个不同事实。

### 4. fork 能否复制父历史中尚无结果的 tool_use？

runAgent 先经过 filterIncompleteToolCalls，避免继承不完整的调用/结果轨迹。fork 得到起始历史，不等于父子从此共享同一个可变消息数组，也不等于建立操作系统沙箱。

### 5. async_launched 是否就是 completed？

不是。AgentTool 的结果映射分别处理启动状态与完成内容。接到启动确认时，编排者仍欠一个后续结果；这个原则也适用于自己的后台任务系统。

### 6. 自动压缩连续失败，会自动终止整个循环吗？

autoCompactIfNeeded 的熔断让后续压缩尝试不再执行；它本身没有终止整个 queryLoop。是否还有超限恢复、错误返回等，必须追到调用方。局部保护不等于全局完成条件。

## 最后把源码结论接回教程

- 循环、状态、重试：第[四](../lessons/04-state.md)、[六](../lessons/06-agent-loop.md)、[八](../lessons/08-retry.md)课
- 子代理与结果责任：第[十七](../lessons/17-why-multi-agent.md)、[十八](../lessons/18-manager-and-tools.md)、[十九](../lessons/19-handoff.md)课
- 并发与权限：第[二十](../lessons/20-parallel.md)、[二十三](../lessons/23-human-approval.md)、[二十七](../lessons/27-boundaries.md)课
- 当前产品行为：案例[七](../cases/07-claude-code-runtime.md)、[八](../cases/08-claude-code-collaboration.md)；官方组件路线：案例[九](../cases/09-claude-code-source-reading.md)

历史代码最有用的部分，是让你看到边界怎样落成分支和状态；不能用它替代当前文档，也不能用当前文档抹掉历史实现里确实存在的机制。

