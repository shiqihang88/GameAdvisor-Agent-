from agent.llm import chat
from agent.tools import TOOLS
import json
from datetime import datetime

# 工具映射
TOOL_MAP = {}

def _load_tool_map():
    from services.ad_manager import ad_safe_adjust_bid, ad_adjust_budget, ad_pause_campaign, get_all_active_campaigns, get_campaign
    from services.feishu_bot import send_feishu_message
    global TOOL_MAP
    TOOL_MAP = {
        "get_campaign_performance": lambda campaign_id=None: 
            [c.dict() for c in get_all_active_campaigns()] if not campaign_id else get_campaign(campaign_id).dict() if get_campaign(campaign_id) else "未找到",
        "adjust_bid": ad_safe_adjust_bid,
        "adjust_budget": ad_adjust_budget,
        "pause_campaign": ad_pause_campaign,
        "send_feishu_message": send_feishu_message,
    }

_load_tool_map()

SYSTEM_PROMPT = """
你是一个专业的游戏广告投流AI助手，名字叫 GameAdvisor。你可以获得实时广告数据，并安全地调整出价、预算，或暂停广告系列。
所有涉及资金的操作务必先考虑安全规则：
- 单次调价不超过当前出价的20%
- 预算调整不超过30%
- 每日同一系列调价最多50次
- 当你完成操作后，必须调用 send_feishu_message 将操作结果与决策依据通知用户。
- 如果用户输入模糊，请询问具体系列或数值。
当前时间：{current_time}
""".strip()

def handle_user_message(user_text: str, conversation_history: list = None) -> str:
    if conversation_history is None:
        conversation_history = []
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.format(current_time=datetime.now().isoformat())},
        *conversation_history,
        {"role": "user", "content": user_text}
    ]
    
    # 第一轮调用模型
    response = chat(messages, tools=TOOLS)
    
    # 如果有工具调用，执行并再次调用模型
    while response.tool_calls:
        # 将模型回复加入消息历史
        messages.append(response.model_dump())
        
        for tool_call in response.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            
            func = TOOL_MAP.get(func_name)
            if func:
                try:
                    result = func(**func_args)
                    result_str = json.dumps(result, ensure_ascii=False, default=str)
                except Exception as e:
                    result_str = f"工具执行错误: {str(e)}"
            else:
                result_str = f"未知工具 {func_name}"
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result_str
            })
        
        # 再次调用模型，让它基于工具结果生成最终回复
        response = chat(messages, tools=TOOLS)
    
    # 最终文本回复
    final_msg = response.content
    return final_msg