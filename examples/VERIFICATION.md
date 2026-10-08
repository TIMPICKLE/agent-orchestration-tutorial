# 离线示例验证记录

核对日期：2026-10-08。验证环境：Linux 教学工作区，Python 3.12.14，Python 标准库。没有安装第三方依赖，没有 API key，没有网络请求。以下命令均从仓库根目录执行。

## 实际执行并通过

```bash
python --version
python -m unittest discover -s tests -v
python -m examples.fixed_workflow
python -m examples.bounded_loop
python -m examples.message_delivery
python -m examples.approval_resume
python -m compileall -q examples tests
```

结果：

- Python 版本：`Python 3.12.14`。
- unittest：`Ran 24 tests`，`OK`；首次运行耗时 0.018 秒，时长不是性能基准。
- 四个演示均正常退出，输出与 [README.md](README.md) 所列一致。
- `compileall` 正常退出，无语法错误。

## 断言覆盖

- 固定流程：原始缺陷可复现；修复满足约定语法；单例成功但回归失败的错误补丁被识别；Decimal 小数运算精确。
- 有界循环：失败反馈可观察；修复后的测试通过才结束；立即声称完成被拦截；候选更换使旧证据失效；工具和补丁白名单；动作格式错误；两步预算耗尽及零预算。
- 消息交付：重复消息不生成重复副作用；相同 ID 不同内容被拒绝；模拟服务完成副作用后丢失响应；关闭并重开双方 SQLite 连接后成功对账；幂等重复调用；外部内容冲突；未知 outbox 键。
- 审批恢复：未审批无副作用；JSON 保存/加载；已批准内容可模拟发布；同一批准重复恢复不重复创建内存工件；内容、版本、任务、动作或目标改变使批准失效。

总计 24 个测试方法，其中部分使用 subTest 验证多个输入。

## 没有验证，不能据此推断

- 没有调用任何真实大模型；ScriptedFakeModel 是固定脚本。
- 没有安装或运行 LangGraph、OpenAI Agents SDK、Claude Agent SDK、MCP 或其他框架。
- 没有连接 Azure DevOps、GitHub、真实邮件或消息服务。
- 只验证单写者、顺序消费；没有做并发消费者压力或竞态测试。
- 没有测试真正的进程崩溃、断电、网络分区、多 worker 竞争、认证或审批身份防伪。
- SQLite 重开证明这里的数据持久化路径可读，不等于生产级分布式事务保证。
- 审批示例的 FakeReviewProvider 只有内存状态；不能证明跨进程发布幂等。
- 教程正文中的框架示意代码不在本次 Python 文件语法检查范围内；是否另行检查见正文的总验证记录。

所有模拟数据都由示例生成。SQLite/JSON 演示使用 TemporaryDirectory，结束时自动清理；`compileall` 只产生可删除的 `__pycache__` 缓存。
