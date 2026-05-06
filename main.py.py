from fastapi import FastAPI, Request, HTTPException
import json
from agent.central_agent import handle_user_message

app = FastAPI(title="GameAdvisor Agent")

# 飞书事件验证
@app.get("/feishu/event")
async def verify_url(token: str, challenge: str = None, type: str = None):
    from config import FEISHU_VERIFY_TOKEN
    if token != FEISHU_VERIFY_TOKEN:
        raise HTTPException(status_code=403, detail="invalid token")
    if challenge:
        return {"challenge": challenge}
    return "ok"

# 接收飞书消息
@app.post("/feishu/event")
async def feishu_event(request: Request):
    # 简化解析：真实飞书回调包含 header 和 body，需解密等，此处演示核心逻辑
    body = await request.json()
    # 实际应按飞书文档处理 challenge，这里只处理消息接收
    if "challenge" in body:
        return {"challenge": body["challenge"]}
    
    # 提取消息文本（具体字段需参考飞书文档）
    try:
        event = body.get("event", {})
        if event.get("type") == "message":
            message_content = event.get("message", {}).get("content", "")
            # 若内容为 JSON 字符串，解析出 text
            if isinstance(message_content, str):
                content_obj = json.loads(message_content)
                text = content_obj.get("text", "")
            else:
                text = message_content.get("text", "")
            
            # 调用 Agent
            reply = handle_user_message(text)
            # 回复消息（需有 bot 发送权限，此处简化返回）
            return {"reply": reply}
    except Exception as e:
        reply = f"处理异常: {str(e)}"
    return {"reply": reply}

# 测试接口：手动触发 Agent
@app.get("/test")
async def test_instruction(text: str):
    reply = handle_user_message(text)
    return {"reply": reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)