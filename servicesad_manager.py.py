from models import CampaignStatus
from config import MAX_SINGLE_BID_CHANGE_PCT, MAX_DAILY_BID_CHANGES, MAX_BUDGET_CHANGE_PCT
from datetime import datetime, date
import copy

# 模拟数据库
fake_campaigns = {
    "cmp001": CampaignStatus(
        campaign_id="cmp001", name="斗罗大陆-安卓-激励视频",
        budget=5000.0, current_bid=1.2, roi=0.85,
        impressions=12000, clicks=360, conversions=40,
        status="active", last_modified=datetime.now(), daily_bid_changes=0
    ),
    "cmp002": CampaignStatus(
        campaign_id="cmp002", name="原神-ios-信息流",
        budget=8000.0, current_bid=2.0, roi=1.15,
        impressions=25000, clicks=800, conversions=65,
        status="active", last_modified=datetime.now(), daily_bid_changes=3
    ),
}

today_date = date.today()

def get_all_active_campaigns():
    return [c for c in fake_campaigns.values() if c.status == "active"]

def get_campaign(campaign_id: str):
    return fake_campaigns.get(campaign_id)

def update_campaign(campaign_id: str, updates: dict):
    camp = fake_campaigns.get(campaign_id)
    if not camp:
        return False
    for k, v in updates.items():
        setattr(camp, k, v)
    camp.last_modified = datetime.now()
    return True

def ad_safe_adjust_bid(campaign_id: str, new_bid: float) -> str:
    camp = get_campaign(campaign_id)
    if not camp:
        return f"广告系列 {campaign_id} 不存在"
    if camp.daily_bid_changes >= MAX_DAILY_BID_CHANGES:
        return f"已超过每日调价上限 ({MAX_DAILY_BID_CHANGES}次)，操作被拦截"
    change_pct = abs(new_bid - camp.current_bid) / camp.current_bid
    if change_pct > MAX_SINGLE_BID_CHANGE_PCT:
        return f"单次调价幅度 {change_pct:.1%} 超过安全阈值 {MAX_SINGLE_BID_CHANGE_PCT:.1%}，操作被拦截"
    # 模拟真实 API 调用
    update_campaign(campaign_id, {
        "current_bid": round(new_bid, 2),
        "daily_bid_changes": camp.daily_bid_changes + 1
    })
    return f"已成功将 {camp.name} 出价调整为 {new_bid:.2f} 元"

def ad_adjust_budget(campaign_id: str, new_budget: float) -> str:
    camp = get_campaign(campaign_id)
    if not camp:
        return f"广告系列 {campaign_id} 不存在"
    change_pct = abs(new_budget - camp.budget) / camp.budget
    if change_pct > MAX_BUDGET_CHANGE_PCT:
        return f"预算调整幅度 {change_pct:.1%} 超过安全阈值"
    update_campaign(campaign_id, {"budget": new_budget})
    return f"已将 {camp.name} 日预算调整为 {new_budget:.2f} 元"

def ad_pause_campaign(campaign_id: str, reason: str) -> str:
    camp = get_campaign(campaign_id)
    if not camp:
        return "系列不存在"
    update_campaign(campaign_id, {"status": "paused"})
    return f"已暂停 {camp.name}，原因：{reason}"