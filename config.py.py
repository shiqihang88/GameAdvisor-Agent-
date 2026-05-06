import os
from dotenv import load_dotenv

load_dotenv()

# 大模型配置 (兼容 OpenAI 接口)
LLM_API_KEY = os.getenv("LLM_API_KEY", "sk-xxx")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")

# 飞书配置
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET")
FEISHU_VERIFY_TOKEN = os.getenv("FEISHU_VERIFY_TOKEN")
FEISHU_BOT_WEBHOOK = os.getenv("FEISHU_BOT_WEBHOOK")  # 发送消息的 webhook

# 安全边界
MAX_SINGLE_BID_CHANGE_PCT = 0.2   # 单次调价幅度不超过20%
MAX_DAILY_BID_CHANGES = 50        # 单广告系列每日调价次数上限
MAX_BUDGET_CHANGE_PCT = 0.3       # 预算调整幅度上限