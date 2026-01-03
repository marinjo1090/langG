from app.graph import app

def main():
    print("--- 歡迎來到 LangGraph 測試 (輸入 'exit' 退出) ---")
    while True:
        user_input = input("你: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            break
            
        # 呼叫圖
        inputs = {"messages": [("user", user_input)]}
        for event in app.stream(inputs):
            for value in event.values():
                # 印出最後一條 AI 回覆
                print("AI:", value["messages"][-1].content)

if __name__ == "__main__":
    main()