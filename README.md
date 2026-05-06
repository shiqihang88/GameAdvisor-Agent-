# GameAdvisor-Agent-
构建基于大模型的 “中央调度Agent + 专项技能Agent集群” ，深度打通企业微信/飞书与广告API，实现： “数据驱动 — Agent决策 — 自动化执行 — 即时协同” 的闭环。
安装依赖
技术架构（简版，体现专业度）
text
[广告平台API] ⇄ [数据中台] ⇄ [Agent大脑(大模型+规则引擎)]
        ↕
[执行器集群] ←→ [中央调度Agent] ←→ [企业微信/飞书 Bot]
        ↕
[素材库/知识库]            [通知/审批/指令交互]
中央调度Agent：基于ReAct框架，负责意图理解、任务拆解、冲突仲裁

数据分析Agent：实时监测ROI、LTV、留存率等核心指标，异常检测

策略Agent：根据历史数据和业务规则，生成调价、预算分配、素材更替建议

执行Agent：调用广告平台开放API，自动完成出价修改、预算调整、广告启停

企微/飞书交互Agent：将决策过程推送至群聊，接收自然语言指令（如“把A素材预算加20%”），形成双向沟通

主要功能模块
智能盯盘预警 — 多维度实时监控，异动自动触发策略调整

ROI最大化自动调优 — 基于强化学习思路的预算动态分配

素材生命周期管理 — 自动识别衰退素材，触发换新及A/B测试任务

对话式工作台 — 在企微/飞书内用自然语言查询数据、下达指令、审批高风险操作

自动化日报/归因 — 每日自动生成多维度汇报，标记AI决策与结果，形成可追溯日志
game_advisor_agent/
├── agent/
│   ├── __init__.py
│   ├── central_agent.py      # 中央调度 Agent (ReAct 框架)
│   ├── llm.py                # 大模型接口封装
│   └── tools.py              # 工具函数定义 (供 Agent 调用)
├── services/
│   ├── __init__.py
│   ├── ad_manager.py         # 广告操作模拟 / 真实 API 填充点
│   └── feishu_bot.py         # 飞书消息发送 (真实调用)
├── config.py                 # 配置与常量
├── main.py                   # FastAPI 主服务，接收飞书回调
├── models.py                 # 数据模型
├── requirements.txt
└── .env.example
bash
pip install -r requirements.txt
配置环境变量
复制 .env.example 为 .env 并填入真实值。若仅测试，可不填飞书信息，直接调用 /test 接口。

启动服务

bash
python main.py
测试 Agent
浏览器访问 http://localhost:8000/test?text=查看当前所有广告系列的表现
或发送 text=把 cmp001 的出价降低 10%

接入真实飞书

将 /feishu/event 配置为飞书应用的事件订阅地址。

完善 feishu_event 方法中的消息解析与回复逻辑（飞书 SDK 推荐）。

在飞书开放平台开启机器人能力。

接入真实广告 API
替换 services/ad_manager.py 中的模拟函数，调用巨量引擎、腾讯广告等开放 API，注意保留安全校验层。

核心设计还原
安全熔断：所有资金操作都在 ad_manager.py 中做了比例和频次限制，Agent 本身也会在提示词中强调安全，形成双保险。

ReAct 循环：central_agent.py 实现了“思考→行动→观察→再思考”，模型可以连续调用多个工具。

飞书双向交互：用户可在群内@机器人发送指令，Agent 结果通过 send_feishu_message 推送回群。

可扩展工具：只需在 tools.py 和 TOOL_MAP 中新增函数定义，即可赋予 Agent 新能力（如素材替换、报表生成）。

