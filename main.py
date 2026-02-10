from app.graph import app

def main():
    print("--- 歡迎來到 LangGraph 測試 (輸入 'exit' 退出) ---")
    while True:
        user_input = input("你: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            break
            
        inputs = {"messages": [("user", user_input)]}
        
        # 執行圖並串流結果
        for event in app.stream(inputs):
            for node_name, value in event.items():
                # 增加 value is not None 的檢查
                if value is not None and isinstance(value, dict) and "messages" in value:
                    # 這裡才放你原本處理 last_msg 的邏輯
                    last_msg = value["messages"][-1]
                    
                    # 只有當訊息有內容時才處理
                    if hasattr(last_msg, 'content') and last_msg.content:
                        content = last_msg.content
                        
                        # 處理 Gemini 有時會回傳 list 的情況
                        if isinstance(content, list):
                            for item in content:
                                if isinstance(item, dict) and item.get('type') == 'text':
                                    print(f"AI ({node_name}): {item['text']}")
                        # 處理純字串情況
                        elif isinstance(content, str):
                            # 避免印出空的工具調用訊息
                            if content.strip():
                                print(f"AI ({node_name}): {content}")
                    
                    # 如果是工具調用階段，我們印一條簡單的日誌就好
                    if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
                        for tool_call in last_msg.tool_calls:
                            print(f"--- 系統提示：Agent 決定呼叫工具 [{tool_call['name']}] ---")
if __name__ == "__main__":
    main()