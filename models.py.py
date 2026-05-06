from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class CampaignStatus(BaseModel):
    campaign_id: str
    name: str
    budget: float
    current_bid: float
    roi: float
    impressions: int
    clicks: int
    conversions: int
    status: Literal["active", "paused", "learning"]
    last_modified: datetime
    daily_bid_changes: int = 0   # 当日已调价次数

class UserInstruction(BaseModel):
    """从飞书消息解析的用户指令"""
    raw_text: str
    intent: Optional[str] = None
    campaign_id: Optional[str] = None
    action: Optional[str] = None
    value: Optional[float] = None