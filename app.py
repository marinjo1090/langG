import chainlit as cl
from app.graph import app 
from langchain_core.messages import HumanMessage

@cl.on_chat_start
async def start():
    # 初始化一個全新的對話狀態
    cl.user_session.set("graph_state", {"messages": []})
    await cl.Message(content="藥物安全助手已連線，請問今天想查詢什麼藥物資訊？").send()

@cl.on_message
async def main(message: cl.Message):
    state = cl.user_session.get("graph_state")
    state["messages"].append(HumanMessage(content=message.content))
    
    # 修正 1：給予初始佔位符，避免前端讀到 null
    final_answer = cl.Message(content="思考中...") 

    async for event in app.astream(state, config={"configurable": {"thread_id": "cl_user"}}):
        for node_name, value in event.items():
            async with cl.Step(name=node_name) as step:
                # 預設一個字串，防止 t.trim 報錯
                step.output = "正在處理節點任務..." 
                
                if "messages" in value:
                    last_msg = value["messages"][-1]
                    
                    # 處理工具呼叫
                    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                        step.input = f"決定呼叫工具: {last_msg.tool_calls[0]['name']}"
                    
                    # 修正 2：確保 output 永遠是字串
                    content = last_msg.content if last_msg.content else ""
                    if isinstance(content, list):
                        content = content[0].get("text", "") if content else ""
                    
                    msg_str = str(content)
                    
                    if last_msg.type == "tool":
                        step.output = msg_str if msg_str else "工具執行完畢"
                    
                    if node_name == "verify":
                        step.output = f"驗證結果：{msg_str}"

                    if last_msg.type == "ai" and not last_msg.tool_calls:
                        # 只有當真的有內容時才更新 final_answer
                        if msg_str.strip():
                            final_answer.content = msg_str
                            step.output = "生成最終回覆"

    # 修正 3：如果最後內容還是空的，給個提示以免崩潰
    if not final_answer.content:
        final_answer.content = "抱歉，我暫時無法回應該問題。"
        
    await final_answer.send()
    cl.user_session.set("graph_state", state)