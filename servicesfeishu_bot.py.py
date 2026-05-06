import requests
from config import FEISHU_BOT_WEBHOOK

def send_feishu_message(content: str):
    """向飞书群发送机器人消息"""
    if not FEISHU_BOT_WEBHOOK:
        print("[模拟飞书] 消息内容:", content)
        return "未配置 Webhook，消息已打印"
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": "GameAdvisor 通知"}
            },
            "elements": [
                {"tag": "markdown", "content": content}
            ]
        }
    }
    try:
        r = requests.post(FEISHU_BOT_WEBHOOK, json=payload, timeout=5)
        return r.json()
    except Exception as e:
        return f"发送失败: {str(e)}"