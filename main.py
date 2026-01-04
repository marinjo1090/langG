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
                # 檢查這個節點的回傳值中是否有 messages
                if "messages" in value:
                    # 取得最後一條訊息 (通常是 AI 的回覆)
                    last_msg = value["messages"][-1]
                    # 確保它是 BaseMessage 類型且有內容
                    if hasattr(last_msg, 'content'):
                        print(f"AI ({node_name}):", last_msg.content)
                else:
                    # 如果是 sentiment_node，我們可以印出它的分析結果
                    print(f"--- 節點 {node_name} 執行完畢，目前狀態: {value} ---")

if __name__ == "__main__":
    main()