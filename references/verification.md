# 验证范围与已知限制

[学习路线](../README.md) · [离线实验详细记录](../examples/VERIFICATION.md)

记录日期：2026 年 10 月 8 日。这里把已执行、仅做静态检查、仅阅读来源和设计建议分开。

## 一 已执行的离线实验

环境：Linux 教学工作区，Python 3.12.14，标准库，无第三方依赖安装，无 API key，无网络请求。

实际执行：

```bash
python -m unittest discover -s tests -v
python -m examples.fixed_workflow
python -m examples.bounded_loop
python -m examples.message_delivery
python -m examples.approval_resume
python -m compileall -q examples tests
```

结果：24 个 unittest 测试方法通过；四个演示正常退出；examples 与 tests 的 Python 语法编译通过。完整覆盖与输出见 [详细记录](../examples/VERIFICATION.md)。

这些测试使用预先写好的候选函数、脚本化假模型、假服务和模拟审批。它们验证宿主协议与指定失败场景，不验证真实模型的适应能力。

## 二 框架示意

`framework_samples/` 提供完整装配代码，便于补齐正文省略的初始化、节点注册、工具与恢复调用。

- 没有安装或运行 LangGraph 与 OpenAI Agents SDK 集成。
- 没有真实模型调用或费用测量。
- 没有锁定并验证第三方依赖组合。
- LangGraph 示例用 InMemorySaver，仅意图演示同一进程暂停与恢复。
- Agents SDK 通知示例只操作内存 outbox，没有真实消费者和投递。

正文中的 Python 代码块已用 Python AST 解析检查语法，未发现语法错误。两个完整文件 `langgraph_complete.py` 与 `agents_collaboration.py` 也分别通过 `ast.parse`，检查进程正常退出，未导入或执行框架。这只说明代码能被解析，不说明依赖可导入、变量齐全或 API 能成功执行。短片段仍需相应上下文。

## 三 文档检查

已检查全部课程的相邻课导航、示例文件链接和来源锚点；内部链接检查不代替所有外部网页的可达性保证。

已检查教程中模拟代码、设计建议和真实仓库事实的标签，删除未确认产品身份的替代解释。没有将 README 测试数量写成本次本地重跑结果。

## 四 项目与产品研究

- `devops-agent-chassis`：读取固定公开提交，并查询指定 GitHub Actions 状态；未本地重新运行项目测试。
- `AzureCodeAgent_Pure_Agent_Drive`：获准公开相关架构分析，读取指定私有提交；未启动服务或执行真实任务，公众可能无法访问源仓库。
- Multica：阅读固定提交相关文档与源码；未安装运行、压力测试或安全审计。
- Meta Muse：阅读官方产品与工程披露；未实测，也未审计未公开源码。

具体提交、入口和证据边界见 [来源索引](sources.md)。

## 五 这些结果不能证明什么

不能证明真实 Azure DevOps、GitHub、CI、邮件或消息渠道已经集成；不能证明真实用户认证、权限撤销、网络分区、多 worker 竞争和进程崩溃都正确处理。

消息实验只覆盖单写者和顺序消费。数据库连接重开不等于断电演练。审批示例的假发布端只保存内存状态，不能证明跨进程发布幂等。

测试通过也不代表可以直接部署生产或获得发布授权。将教程设计转为实际系统时，需要补上与所选环境、服务和组织策略对应的集成及故障验证。
