"""Advanced tutorial figures: collaboration, delivery and case-study boundaries."""
from pathlib import Path
from diagram_lib import Figure, PALETTE


def build(root):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)

    f = Figure('18-expert-call', '专家返回，管理者继续', '子任务调用：整体责任仍在管理者', 740)
    f.node(32, 130, 264, '管理者', '负责工单 1042', role='model')
    f.node(344, 296, 264, '只读审查专家', '返回发现与证据', role='model')
    f.node(32, 462, 264, '管理者继续', '修复、验证或报告', role='model')
    f.path('M296,186 L320,186 L320,352 L344,352')
    f.text(46, 278, '调用：问题、候选、证据', 24)
    f.path('M344,380 L322,380 L322,518 L296,518')
    f.text(352, 446, '结果回到管理者', 24)
    f.note(594, ['必须审查？由程序设为必经步骤。'], role='program')
    f.save(root)

    f = Figure('19-handoff-compare', '调用、通知、交接控制', '三个协议，三种不同的责任关系', 790)
    f.text(32, 136, '① 工具调用：等专家返回', 28, bold=True)
    f.node(32, 160, 218, '管理者', role='model', h=92)
    f.node(390, 160, 218, '专家', role='model', h=92)
    f.line(250, 187, 390, 187, arrow=True)
    f.text(290, 174, '调用', 24)
    f.line(390, 230, 250, 230, arrow=True)
    f.text(290, 262, '返回', 24)
    f.text(32, 316, '② 通知：传信息，不代表接管', 28, bold=True)
    f.node(32, 340, 218, '发送者', role='model', h=92)
    f.node(390, 340, 218, '接收者', role='model', h=92)
    f.line(250, 386, 390, 386, arrow=True)
    f.text(278, 369, '消息', 24)
    f.text(32, 496, '③ handoff：接收者继续当前运行', 28, bold=True)
    f.node(32, 520, 218, '分诊助手', role='model', h=92)
    f.node(390, 520, 218, '验收助手', role='model', h=92)
    f.line(250, 566, 390, 566, arrow=True)
    f.text(270, 548, '控制权', 24)
    f.note(645, ['业务负责人和权限仍由应用定义。'], role='program')
    f.save(root)

    f = Figure('20-parallel-join', '并行之后，先对齐再汇总', '示例：两个必需的只读审查任务', 810)
    f.node(184, 125, 272, '同一候选 B', '先核对范围与预算', role='program')
    f.path('M320,237 L320,267 L172,267 L172,296')
    f.path('M320,267 L468,267 L468,296')
    f.node(32, 296, 280, '格式审查完成', '版本 B · 有证据', role='model')
    f.node(328, 296, 280, '覆盖审查超时', '必需结果仍缺失', role='risk')
    f.path('M172,408 L172,456 L320,456 L320,485')
    f.path('M468,408 L468,456 L320,456', dash=True, arrow=False)
    f.node(96, 485, 448, '程序汇总检查', '版本一致？证据齐全？存在冲突？', role='program')
    f.arrow(597, 627)
    f.note(633, ['保留已完成结果，并报告缺失。', '必需分支未完成，不能判整体成功。'], role='risk')
    f.save(root)

    f = Figure('21-event-run-result', '收到、唤醒、执行、成功', '四个阶段，各自需要可核验的证据', 860)
    stages = [
        (1, '事件收到', '入口保存事件与关联 ID', 'external'),
        (2, '运行被唤醒', '建立或恢复对应 run_id', 'program'),
        (3, '动作已执行', '工具留下动作与结果记录', 'program'),
        (4, '任务成功', '当前产物满足验收标准', 'program'),
    ]
    for i, (n, title, detail, role) in enumerate(stages):
        y = 122 + i * 132
        f.dot(58, y + 48, n, role)
        f.node(104, y, 504, title, detail, role=role, h=108)
        if i < 3:
            f.line(58, y + 72, 58, y + 154, arrow=True)
    f.note(674, ['HTTP 200 和 Run 结束，都不能', '单独证明业务任务已经成功。'], role='risk')
    f.save(root)

    f = Figure('22-outbox-uncertainty', '消息发出，确认却丢失', '发送成功与本地知道成功，是两回事', 920)
    f.node(32, 124, 268, '持久待发箱', '稳定消息 ID：M7', role='program')
    f.node(344, 124, 264, '接收服务', '按协议接收消息', role='external')
    f.line(166, 236, 166, 650, color='#126653', dash=True)
    f.line(476, 236, 476, 650, color='#684699', dash=True)
    f.line(166, 286, 476, 286, arrow=True)
    f.text(207, 269, '发送 M7', 24)
    f.text(488, 317, '已接收', 24, color='#684699')
    f.line(476, 350, 286, 350, dash=True, arrow=True)
    f.text(292, 387, '确认回复丢失', 24, color='#a13325')
    f.text(170, 403, '×', 36, bold=True, color='#a13325')
    f.node(32, 433, 268, '本地：结果未知', '先查询，不盲目重发', role='risk')
    f.line(300, 492, 476, 492, arrow=True)
    f.text(314, 471, '查询 M7', 24)
    f.line(476, 602, 166, 602, arrow=True)
    f.text(207, 584, '核实接收结果', 24)
    f.band(660, '程序保存核实后的状态', '服务接收 ≠ 送达 ≠ 已读', role='program')
    f.note(764, ['查询或幂等重试，须有接收平台支持。'], role='external')
    f.save(root)

    f = Figure('23-approval-binding', '批准必须绑定具体版本', '人、动作、对象、版本，缺一不可', 860)
    f.rect(32, 120, 576, 224, PALETTE['human'][0])
    f.text(52, 155, '人工决定 · 审批卡', 28, bold=True, color=PALETTE['human'][1])
    f.text(52, 199, '批准者：具备该动作权限的人', 26)
    f.text(52, 239, '动作：create_draft_pr', 26)
    f.text(52, 279, '对象：demo-repository', 26)
    f.text(52, 319, '绑定候选：A', 26, bold=True)
    f.arrow(344, 380)
    f.node(32, 390, 268, '当前候选 B', '与审批绑定版本不同', role='neutral')
    f.node(344, 390, 264, '当前任务状态', '有效还是已取消？', role='program')
    f.path('M166,502 L166,536 L320,536 L320,566')
    f.path('M476,502 L476,536 L320,536', arrow=False)
    f.node(80, 566, 480, '执行前重新核验', 'A ≠ B：旧批准不能直接复用', role='program')
    f.note(704, ['任务已取消：记录晚到同意，不执行。'], role='risk')
    f.save(root)

    f = Figure('24-four-identities', '四个身份，分别核对', '可以由同一人兼任，不能直接等同', 738)
    f.node(32, 132, 276, '请求者', '谁提出这项工作？', role='human', h=142)
    f.node(332, 132, 276, '资产 owner', '仓库与连接属于谁？', role='human', h=142)
    f.node(32, 356, 276, '执行 Agent', '谁承担具体工作？', role='model', h=142)
    f.node(332, 356, 276, '审批者', '谁能批准目标动作？', role='human', h=142)
    f.line(170, 274, 170, 356, arrow=True)
    f.text(190, 324, '分配', 24)
    f.line(470, 274, 470, 356, dash=True, arrow=False)
    f.text(368, 324, '另行核对', 24)
    f.line(332, 427, 308, 427, arrow=True)
    f.note(544, ['执行前核对实际账户、目标与权限。', '能发任务，不代表能借用全部凭据。'], role='program')
    f.save(root)

    f = Figure('30-evidence-chain', '把每一段交付与版本连起来', '虚构流程：每条边都需要可核验的关联', 1040)
    data = [
        ('工单 1042', '范围、验收条件、基线版本', 'neutral'),
        ('候选 B 与测试 B', '测试记录对应当前候选', 'program'),
        ('PR 与构建', 'PR head B ↔ build ID', 'external'),
        ('测试包与人工结论', '包摘要、来源、验收结果', 'human'),
        ('具体动作的授权记录', '执行前再核对目标与当前版本', 'human'),
    ]
    for i, (title, detail, role) in enumerate(data):
        y = 120 + i * 144
        f.node(88, y, 464, title, detail, role=role)
        if i < 4:
            f.arrow(y + 112, y + 138)
    f.note(854, ['质量通过与操作授权，要分别记录。', '任务只到本地补丁，就在相应处停止。'], role='program')
    f.save(root)

    f = Figure('c01-fact-vs-design', '源码事实与设计建议分开看', 'devops-agent-chassis：固定版本案例', 810)
    f.rect(32, 126, 278, 470, '#e8f6f2')
    f.rect(330, 126, 278, 470, '#fff3d9')
    f.text(52, 166, '已见于源码', 28, bold=True, color='#126653')
    f.text(350, 166, '仍需应用核查', 28, bold=True, color='#885800')
    for y, a, b in [
        (222, '任务源与编排器', '真实执行工具路径'),
        (262, '独立完成判据', '是否强制检查权限'),
        (348, '默认内存账本', '长期任务怎样恢复'),
        (388, '可选 JSON 存储', '并发与事务是否可靠'),
        (474, '可装配接口', '外部动作如何对账'),
        (514, '多种推理模式', '业务证据是否独立'),
    ]:
        f.text(52, y, a, 24)
        f.text(350, y, b, 24)
    f.text(52, 567, '程序控制 · 当前实现', 22, color='#126653', bold=True)
    f.text(350, 567, '人工决定 · 设计取舍', 22, color='#885800', bold=True)
    f.note(626, ['增加推理模式，不能代替可靠存储。', '下一步对准实际失败，而非接口数量。'], role='risk')
    f.save(root)

    f = Figure('c02-session-verifier', '保留自主会话，补交付核验', 'Pure Agent Drive：当前事实与新增建议', 860)
    f.text(32, 136, '当前：外层检查运行与报告协议', 28, bold=True)
    f.node(32, 158, 272, 'CLI 自主会话', '内部组织调查与修复', role='model')
    f.node(344, 158, 264, '记录终态', '协议与进程结果检查', role='program')
    f.line(304, 214, 344, 214, arrow=True)
    f.note(298, ['协议有效，不等于独立业务测试通过。'], role='risk')
    f.text(32, 411, '建议新增：只读交付核验点', 28, bold=True)
    f.node(32, 435, 272, '会话交付', '候选 SHA、PR、证据', role='model')
    f.node(344, 435, 264, '只读核验器', '查远端与同版本检查', role='program')
    f.line(304, 491, 344, 491, arrow=True)
    f.arrow(547, 600, x=476)
    f.band(607, '缺失或旧证据：阻塞或返工', '不凭会话自述，直接宣布交付正确', role='risk')
    f.note(710, ['下半图是建议，尚非该版本已有能力。'], role='human')
    f.save(root)

    f = Figure('c03-muse-boundary', '主动行动，也要逐步过门', 'Meta Muse：据公开职责构造的教学模型', 1008)
    f.node(128, 122, 384, '事件或时间触发', '找到相关任务与状态', role='program')
    f.arrow(234, 260)
    f.node(128, 270, 384, '模型提出动作', '结合目标与当前证据', role='model')
    f.arrow(382, 408)
    f.node(128, 418, 384, '执行端权限检查', '允许后执行并保存结果', role='program')
    f.arrow(530, 556)
    f.node(128, 566, 384, '通知价值判断', '重要变化？需要用户决定？', role='program')
    f.path('M240,678 L240,724 L164,724 L164,754')
    f.path('M400,678 L400,724 L476,724 L476,754')
    f.text(41, 706, '值得打断', 24)
    f.text(469, 706, '普通日志', 24)
    f.node(32, 754, 264, '通知用户', '核对渠道与内容范围', role='program')
    f.node(344, 754, 264, '保留活动记录', '无需逐条打断人', role='external')
    f.text(32, 919, '职责示意，非内部调用图，也未经亲测。', 24, color='#4a5768')
    f.save(root)

    f = Figure('c04-multica-identities', '长期任务，可以经历短运行', 'Multica：身份、Issue 与 Run 分开', 880)
    f.band(120, 'Agent：长期身份、owner 与配置', '一次运行结束，不会抹掉这个身份', role='model')
    f.band(225, 'Issue：长期目标、讨论与进度', '多个 Agent 与多次 Run 可参与同一任务', role='external')
    f.line(76, 348, 76, 692, color='#4a5768', arrow=True)
    f.text(34, 716, '时间', 24, color='#4a5768')
    for i, (title, detail) in enumerate([
        ('Run 1 · leader', '委派后结束本轮'),
        ('Run 2 · 成员', '执行子任务并交结果'),
        ('Run 3 · leader', '相关事件触发新一轮汇总'),
    ]):
        y = 340 + i * 126
        f.dot(76, y + 47, i + 1, 'program', r=21)
        f.node(128, y, 480, title, detail, role='program', h=108)
    f.note(727, ['Run 结束，仍需判断 Issue 是否达标。'], role='risk')
    f.save(root)

    f = Figure('c04-mention-vs-inbox', 'Agent 触发与人类通知分两路', 'Multica：接收对象不同，平台语义也不同', 828)
    f.text(32, 136, 'Agent 路径：启动一次具体执行', 28, bold=True)
    f.node(32, 160, 276, '结构化 mention', '目标由平台识别', role='external')
    f.node(348, 160, 260, '按规则创建 Run', '随后由运行时执行', role='program')
    f.line(308, 216, 348, 216, arrow=True)
    f.note(300, ['普通文字 @名字，不自动等同结构化触发。'], role='risk')
    f.text(32, 415, '人类路径：展示通知，再由人查看', 28, bold=True)
    f.node(32, 439, 276, '人类 inbox', '通知进入可见界面', role='external')
    f.node(348, 439, 260, '人查看通知', '出现不等于已读', role='human')
    f.line(308, 495, 348, 495, arrow=True)
    f.note(586, ['Agent 没有人类式 inbox。', '帮助型 mention 不必改变任务负责人。'], role='program')
    f.text(32, 732, '图中省略校验；并非每次提及都创建新 Run。', 24, color='#4a5768')
    f.save(root)

    f = Figure('c05-multica-wakeup', '任务在库里，通道提示有活', 'Multica：实时提示与轮询都指向任务库', 980)
    f.node(128, 120, 384, '数据库：事实来源', '持久保存任务与 Run', role='external')
    f.path('M226,232 L226,276 L168,276 L168,308')
    f.path('M472,308 L472,276 L414,276 L414,232', dash=True)
    f.text(57, 262, '有新任务', 24)
    f.text(456, 262, '兜底查询', 24)
    f.node(32, 308, 272, '实时提示', '告诉 daemon 有活', role='program')
    f.node(336, 308, 272, '轮询路径', '提示丢失仍可检查', role='program')
    f.path('M168,420 L168,461 L320,461 L320,493')
    f.path('M430,493 L430,461 L472,461 L472,420', dash=True)
    f.node(112, 493, 416, 'daemon 领取并执行', '检查绑定、状态与并发条件', role='program')
    f.arrow(605, 635)
    f.node(112, 645, 416, '有条件地写回结果', '仍属有效领取，才允许更新', role='program')
    f.note(788, ['旧领取者迟到，不能覆盖新的状态。', '数据库锁不保证外部动作恰好一次。'], role='risk')
    f.save(root)

    f = Figure('c06-authority-layers', '四种权限边界，分别验证', 'Multica：调用权不能代替执行限制', 870)
    gates = [
        ('启动权限', '谁可以启动这个 Agent？', 'human'),
        ('平台 API 身份', '这轮 Run 在平台内能做什么？', 'program'),
        ('操作系统权限', '进程能读写哪里、访问什么网络？', 'program'),
        ('外部连接权限', '用谁的账户，以及哪些能力？', 'external'),
    ]
    for i, (title, detail, role) in enumerate(gates):
        y = 122 + i * 131
        f.dot(58, y + 48, i + 1, role)
        f.node(103, y, 505, title, detail, role=role, h=108)
        if i < 3:
            f.line(58, y + 72, 58, y + 153, arrow=True)
    f.note(678, ['该版本默认继承 daemon 系统用户权限。', '不承诺统一沙箱；人审不能补上这道边界。'], role='risk')
    f.save(root)

    f = Figure('c07-claude-loop', 'Claude Code：模型选，运行时做', '依据官方文档概念化，并非内部函数调用图', 798)
    f.node(32, 136, 264, '当前上下文', '运行时组装本轮输入', role='neutral')
    f.node(344, 136, 264, '模型选择工具', '依据目标与已有观察', role='model')
    f.line(296, 192, 344, 192, arrow=True)
    f.node(344, 350, 264, '运行支架', '权限策略与执行安排', role='program')
    f.node(32, 350, 264, '工具与环境', '执行并返回观察', role='external')
    f.line(476, 248, 476, 350, arrow=True)
    f.text(490, 310, '工具请求', 24)
    f.line(344, 406, 296, 406, arrow=True)
    f.line(164, 350, 164, 248, arrow=True)
    f.text(38, 310, '观察反馈', 24)
    f.band(516, '会话记录：与当前上下文分开', '本轮所见，不等于完整历史始终放入', role='external')
    f.note(630, ['权限策略不等于每次工具调用都弹窗。', '记录留存与上下文管理，是不同职责。'], role='program')
    f.save(root)

    f = Figure('c07-extension-roles', '四种扩展，各自改变什么', '按需要选部件，不把它们看成同一条流程', 871)
    f.node(32, 132, 276, 'Skill', '按需提供工作指令', role='neutral', h=152)
    f.text(52, 262, '补充步骤与知识', 24, color='#4a5768')
    f.node(332, 132, 276, 'Hook', '在生命周期事件运行', role='program', h=152)
    f.text(352, 262, '触发预设处理', 24, color='#126653')
    f.node(32, 328, 276, 'MCP', '连接外部能力与数据', role='external', h=152)
    f.text(52, 458, '提供工具与资源连接', 24, color='#684699')
    f.node(332, 328, 276, 'Subagent', '委派有限子任务', role='model', h=152)
    f.text(352, 458, '通常有独立上下文', 24, color='#2856a3')
    f.band(526, '共同边界：运行时与权限约束', '扩展能力本身，不等于业务验收', role='program')
    f.note(644, ['fork 可继承起始历史；', '不要假定多个子代理始终共享全部状态。'], role='neutral')
    f.save(root)

    f = Figure('c07-session-scheduling', '恢复会话与定时启动分开看', '依据官方当前文档，具体可用范围请查原文', 911)
    f.band(120, 'resume：继续会话记录', '不会回滚文件修改，也不会撤销外部动作', role='program')
    f.text(32, 260, '定时方式：三张卡各自选择', 28, bold=True)
    f.node(32, 288, 576, '/loop', '需要保持当前会话打开', role='program', h=112)
    f.node(32, 430, 576, 'Desktop 定时任务', '本地机器保持开启，无需会话打开', role='program', h=112)
    f.node(32, 572, 576, 'Cloud routines', '云端运行，无需本地机器在线', role='external', h=112)
    f.note(732, ['再次启动后，仍要核对当前任务、权限', '与外部状态；定时启动不等于正确完成。'], role='risk')
    f.save(root)

    f = Figure('d01-scenario-choice', '按任务选择最小有效方案', '三个独立场景，不是必须走完的升级路线', 830)
    cards = [
        (124, '机械修复', '确定规则转换 + 独立测试', 'program', '失败证据：误改、漏修、过多人工特例'),
        (306, '根因未知的 bug', '受限自主会话 + 独立交付核验', 'model', '失败证据：旧证据、中断丢任务、重复 PR'),
        (488, '多人协作任务板', '身份与归属 + 事件驱动调度', 'human', '失败证据：无人收尾、越权、迟到覆盖'),
    ]
    for y, title, detail, role, failure in cards:
        f.node(32, y, 576, title, detail, role=role)
        f.text(52, y + 145, failure, 24, color='#4a5768')
    f.note(680, ['只有观察到明确失败，才增加对应复杂度。'], role='program')
    f.save(root)


if __name__ == '__main__':
    build(Path(__file__).resolve().parents[1] / 'assets' / 'diagrams')
