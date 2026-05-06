TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_campaign_performance",
            "description": "获取指定广告系列或所有活跃系列的实时数据，包括 ROI、点击、花费等",
            "parameters": {
                "type": "object",
                "properties": {
                    "campaign_id": {
                        "type": "string",
                        "description": "广告系列 ID，若为空则返回所有活跃系列"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "adjust_bid",
            "description": "调整指定广告系列的出价（受安全规则限制）",
            "parameters": {
                "type": "object",
                "properties": {
                    "campaign_id": {"type": "string"},
                    "new_bid": {"type": "number", "description": "新出价，单位元"}
                },
                "required": ["campaign_id", "new_bid"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "adjust_budget",
            "description": "调整广告系列日预算",
            "parameters": {
                "type": "object",
                "properties": {
                    "campaign_id": {"type": "string"},
                    "new_budget": {"type": "number", "description": "新日预算，单位元"}
                },
                "required": ["campaign_id", "new_budget"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "pause_campaign",
            "description": "暂停表现不佳的广告系列",
            "parameters": {
                "type": "object",
                "properties": {
                    "campaign_id": {"type": "string"},
                    "reason": {"type": "string"}
                },
                "required": ["campaign_id", "reason"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_feishu_message",
            "description": "向飞书群发送消息，用于通知、请求审批或汇报结果",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "消息内容，支持 markdown"}
                },
                "required": ["content"]
            }
        }
    }
]