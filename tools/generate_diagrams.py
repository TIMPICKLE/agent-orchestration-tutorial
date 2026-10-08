"""Rebuild the tutorial's original SVG figures with Python's standard library.

Run from any directory: python tools/generate_diagrams.py
For optional mobile-size PNG review, see render_diagrams.py.
"""
from pathlib import Path
from diagram_lib import Figure
ROOT=Path(__file__).resolve().parents[1]/'assets/diagrams'
ROOT.mkdir(parents=True,exist_ok=True)

f=Figure('00-learning-map','先学会一个闭环，再增加能力','阅读层次，不是必须依次升级的架构',786)
for y,n,t,d,r in [(127,'1','基础','任务 → 控制 → 状态','neutral'),(249,'2','执行','固定步骤 → 反馈循环','neutral'),(371,'3','运行','图路由 → 等待恢复','neutral'),(493,'4','协作','委派 → 汇总 → 通知','neutral')]:
 f.dot(59,y+48,n,r); f.node(101,y,507,t,d,r,h=106)
f.band(625,'证据与权限：贯穿所有层',role='human');f.save(ROOT)

f=Figure('01-task-contract','把“修好”拆成可检查的约定','工单1042：四张卡一起定义任务契约',742)
for y,n,t,d,r in [(125,'1','输入','工单1042 + 基线版本','neutral'),(249,'2','交付','补丁 + 说明；到此停止','program'),(373,'3','证据','当前版本的测试记录','external'),(497,'4','权限','工作区修改；发布另批','human')]:
 f.dot(59,y+48,n,r);f.node(102,y,506,t,d,r,h=106)
f.text(32,657,'测试通过，不能自动扩大允许动作。',26,bold=True);f.save(ROOT)

f=Figure('02-control-zones','谁决定下一步：两层控制','程序选阶段；模型在阶段内选择工具',940)
f.node(32,122,576,'进入修复阶段','外层决定阶段，并检查预算','program')
f.arrow(234,276,'交付目标与边界')
f.rect(32,285,576,314,'#f7f9fc','#ced8e5',dash=True)
f.text(52,323,'阶段内部：受限探索',26,bold=True)
f.node(68,342,404,'选择下一次工具','读文件？改代码？运行测试？','model')
f.arrow(454,488,'建议动作')
f.node(68,492,404,'校验后执行工具','返回具体观察结果','program',h=88)
f.path('M472,536 L567,536 L567,397 L480,397')
f.text(499,477,'反馈',24,anchor='middle')
f.arrow(599,634,'提交阶段结果与证据')
f.band(642,'程序验收 → 选择下一阶段',role='program')
f.node(32,751,576,'遇到新权限：等待人','不能靠继续推理跨过审批边界','human');f.save(ROOT)

f=Figure('03-tool-roundtrip','工具请求怎样变成真实执行','模型提出请求；运行时与工具端真正执行',924)
for i,(t,d,r) in enumerate([
 ('请求 run_tests(target)','产生结构化工具调用','model'),
 ('映射函数、校验参数','核对权限和当前任务范围','program'),
 ('工具实际执行','返回退出码与测试输出','external'),
 ('关联原调用，进入下一轮','具体结果成为新的模型输入','program')]):
 y=126+i*170;f.node(52,y,536,t,d,r)
 if i<3:f.arrow(y+112,y+163,['调用请求','允许执行','调用ID + 结果'][i])
f.text(32,830,'只说“我会测试”，不会自动执行工具。',26,bold=True);f.save(ROOT)

f=Figure('04-state-shelves','聊天、任务状态、产物各放哪里','三者互相引用，但不能互相替代',827)
for y,t,d,r in [(126,'对话上下文','为什么这样修改；讨论与观察','model'),(277,'工作流状态','1042 / testing / attempt=1','program'),(428,'产物与版本','补丁、测试日志、候选版本','external')]:
 f.node(52,y,536,t,d,r)
f.line(32,578,608,578,color='#a13325',dash=True);f.text(320,617,'假设现在进程退出',28,anchor='middle',color='#a13325',bold=True)
f.note(649,['只从进程外保存的状态定位产物。','内存字典不提供跨重启恢复。'],'program');f.save(ROOT)

f=Figure('05-fixed-vs-feedback','失败后是否再试，要明确设计','比较“只试一次”和“根据反馈再修改”',850)
f.text(32,147,'A  固定流程：测试后报告',28,bold=True)
for x,t,r in [(32,'提出补丁','model'),(232,'测试','program'),(432,'报告','program')]:
 f.node(x,171,176,t,role=r,h=88)
 if x<432:f.line(x+177,215,x+195,215,arrow=True)
f.note(282,['测试失败也正常报告：只承诺尝试一次。'])
f.text(32,426,'B  反馈流程：失败时带回证据',28,bold=True)
f.node(32,454,252,'提出补丁','新的候选版本','model')
f.node(356,454,252,'测试','具体断言结果','program')
f.line(285,510,348,510,arrow=True)
f.path('M481,567 L481,635 L158,635 L158,574')
f.text(320,624,'失败 + 预算允许',26,anchor='middle')
f.note(681,['通过 → 报告；预算耗尽 → 报告阻塞。'],'program');f.save(ROOT)

f=Figure('06-observation-loop','一轮循环要带回什么','决定 → 执行 → 观察 → 更新，再决定',840)
for y,t,d,r in [(125,'决定：选择下一步','规则决策器或模型都可以','neutral'),(282,'执行：受限工具','程序校验动作、参数和预算','program'),(439,'观察并更新状态','test_failed + 具体断言','external')]:
 f.node(52,y,462,t,d,r)
 if y<439:f.arrow(y+112,y+150,['动作','退出码与日志'][0 if y==125 else 1])
f.path('M514,495 L584,495 L584,181 L522,181')
f.text(566,364,'再选',24,anchor='middle')
f.node(32,619,276,'通过：成功出口','保留对应证据','program')
f.node(332,619,276,'耗尽：阻塞出口','说明剩余问题','program');f.save(ROOT)

f=Figure('07-permission-gate','提示词之外，还要有执行门禁','模型的动作建议，不等于已经获准执行',778)
f.node(64,125,512,'建议 read_file(path)','模型提交动作与参数','model');f.arrow(237,281,'待检查的请求')
f.node(64,292,512,'工具名单 + 参数范围','程序检查真实路径与任务权限','program')
f.path('M320,405 L320,450 L170,450 L170,487');f.path('M320,450 L470,450 L470,487')
f.text(168,442,'允许',24,anchor='middle');f.text(474,442,'拒绝',24,anchor='middle')
f.node(32,501,276,'执行工具','返回实际结果','external')
f.node(332,501,276,'结构化原因','缩小范围或申请授权','program')
f.note(639,['提示词解释意图；执行门禁限制动作。']);f.save(ROOT)

f=Figure('08-retry-triage','同样失败，下一步可能不同','先分类，再决定修复、重试、查询或停止',792)
for y,n,t,d,r in [(124,'1','测试断言失败','修改候选，再验证新版本','model'),(261,'2','执行环境缺少依赖','处理环境，或报告阻塞','program'),(398,'3','网络或进程暂时故障','确认可安全后，有限重试','program'),(535,'4','创建PR后网络断开','可能已经成功：先查询远端','external')]:
 f.dot(58,y+49,n,r);f.node(101,y,507,t,d,r)
f.save(ROOT)
f=Figure('09-two-control-axes','外层生命周期与内层求解，分开选','外层固定，并不排斥内层自主',811)
f.rect(32,125,576,445,'#f7f9fc','#b9c8d8',dash=True)
f.text(52,166,'外层：接单 → 阶段 → 收尾',28,bold=True)
f.text(52,210,'程序管理生命周期与交付边界',24)
f.text(52,266,'内层执行单元，可以分别选择：',26,bold=True)
f.node(62,295,516,'选择A：固定函数','已知规则，确定执行步骤','program')
f.node(62,435,516,'选择B：工具反馈循环','未知路径，允许受限探索','model')
f.note(611,['先写清任务与验收，再选择组合。','图示是设计选项，不是仓库实现清单。']);f.save(ROOT)

f=Figure('10-nested-budgets','外层重试，不重置任务总预算','两种循环：任务尝试与内部工具行动',885)
f.rect(32,125,576,615,'#e8f6f2','#126653',dash=True)
f.text(52,167,'任务总预算：跨尝试累计',28,bold=True,color='#126653')
f.rect(61,198,518,314,'#ffffff','#ced8e5')
f.text(82,241,'外层尝试1',28,bold=True)
f.text(82,284,'准备 → 执行 → 收尾',26)
f.node(82,316,476,'内层行动循环','读 → 改 → 测 → 利用反馈','model')
f.text(82,475,'每个实际动作计入任务消耗',24)
f.arrow(513,550,'若仍可重试')
f.node(61,563,518,'外层尝试2','只使用任务的剩余预算','program')
f.text(52,714,'新尝试 ≠ 免费重开',28,bold=True,color='#126653')
f.save(ROOT)

f=Figure('11-evidence-binding','通过的是A，为什么不能交付B','测试证据只支持它实际验证过的版本',884)
f.node(32,125,270,'候选A','当前内容摘要A','external')
f.node(338,125,270,'测试记录A','通过，绑定摘要A','program')
f.line(303,180,329,180,arrow=True)
f.arrow(237,285,'继续编辑',x=165)
f.node(32,298,270,'候选B','内容已经变化','external')
f.node(338,298,270,'仍是旧记录A','不能证明B通过','risk')
f.line(303,354,330,354,color='#a13325',dash=True)
f.text(320,453,'候选B ≠ 证据绑定的A',30,anchor='middle',bold=True,color='#a13325')
f.node(64,490,512,'重新验证B','核对来源、命令、结果与版本','program')
f.arrow(602,646,'取得B的有效证据')
f.band(659,'再依据任务契约判断交付',role='program')
f.text(32,792,'摘要绑定内容，不自动保证证据可信。',24);f.save(ROOT)

f=Figure('12-session-envelope','给自主会话一个可检查的外壳','把探索交给会话，把验收留给明确规则',877)
f.rect(32,126,576,575,'#f7f9fc','#b9c8d8',dash=True)
f.text(52,166,'外层：预算、结果存储、独立验收',26,bold=True)
f.node(65,195,510,'输入契约','目标 / 允许范围 / 基线版本','program')
f.arrow(307,349,'进入执行会话')
f.node(65,360,510,'会话内部自主探索','读 → 改 → 测 → 根据反馈再选','model')
f.arrow(472,514,'返回产物与证据引用')
f.node(65,525,510,'输出交付包','候选 + 版本 + 证据引用','external')
f.note(733,['外层判断：成功、返工，或明确阻塞。'],'program');f.save(ROOT)

f=Figure('13-graph-vocabulary','节点、状态、边分别回答什么','节点做工作；边依据更新后的状态选路',880)
f.node(52,126,536,'状态：当前知道什么','candidate / passed / attempt','external')
f.arrow(238,286,'节点读取状态')
f.node(52,298,536,'节点 verify：执行验证','普通函数即可，不必是Agent','program')
f.arrow(410,458,'返回更新：passed')
f.node(52,470,536,'边：下一步去哪里','读取更新后的状态进行路由','program')
f.path('M320,583 L320,625 L122,625 L122,665');f.line(320,625,320,665,arrow=True);f.path('M320,625 L518,625 L518,665')
for x,t,d in [(32,'report','报告结果'),(232,'propose','再提候选'),(432,'blocked','报告阻塞')]:
 f.rect(x,680,176,91,'#e8f6f2');f.text(x+88,718,t,26,anchor='middle',bold=True);f.text(x+88,752,d,24,anchor='middle')
f.save(ROOT)

f=Figure('14-state-updates','沿两个节点，看状态字段变化','issue保持不变；candidate与passed被更新',1075)
for y,n,t,lines in [(125,'0','初始状态',['issue = demo-1042','candidate = 空','passed = False']),
 (360,'1','propose之后',['issue = demo-1042','candidate = 候选','passed = False']),
 (595,'2','verify之后',['issue = demo-1042','candidate = 候选','passed = 比较结果'])]:
 f.dot(58,y+42,n);f.rect(101,y,507,188,'#e8f6f2');f.text(121,y+40,t,28,bold=True)
 for j,line in enumerate(lines):f.text(121,y+79+j*36,line,26)
 if y<595:f.arrow(y+188,y+224,'局部更新，其他字段保留')
f.arrow(784,829,'无条件结束边')
f.band(840,'END：结束，但未必成功',role='program')
f.text(32,980,'玩具比较结果，不证明真实解析函数正确。',24);f.save(ROOT)

f=Figure('15-routing-table','路由是有顺序的判断','先看成功，再看剩余尝试次数',916)
f.node(32,124,576,'先读取验证结果','passed 与 attempt','program')
for y,n,t,d in [(278,'1','passed = True','→ report：报告结果'),(441,'2','否则，attempt < 3','→ propose：再提候选'),(604,'3','否则，预算已耗尽','→ blocked：报告阻塞')]:
 f.dot(58,y+43,n);f.node(103,y,505,t,d,'program')
 if y<604:f.arrow(y+112,y+149,'否则')
f.note(759,['模型给出路由时，先验证允许值。','未知值必须拒绝，不自动新增能力。'],'risk');f.save(ROOT)

f=Figure('16-checkpoint-resume','等待跨执行，恢复找到同一状态','持久恢复设计；不是内存saver的保证',1023)
f.node(52,123,536,'执行1：保存等待请求','记录待审批对象，然后interrupt','program')
f.arrow(235,282,'写入进程外存储')
f.node(52,296,536,'持久存储','thread_id + 检查点 + 请求信息','external')
f.line(32,454,608,454,color='#a13325',dash=True)
f.text(320,495,'执行结束，进程可以退出',28,anchor='middle',bold=True,color='#a13325')
f.node(52,542,536,'执行2：验证回复','核对回复人、动作、目标与版本','program')
f.arrow(654,698,'应用验证通过后')
f.node(52,713,536,'使用同一标识恢复','找到原任务与检查点，继续执行','program')
f.note(855,['节点开头可能重跑；副作用仍需去重。','checkpoint不保证外部动作恰好一次。']);f.save(ROOT)

from diagrams_advanced import build
build(ROOT)
print(f'Generated {len(list(ROOT.glob("*.svg")))} tutorial figures in {ROOT}')
