import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from .state import AgentState

load_dotenv() # 自動抓取 .env 裡面的 KEY
from langchain_google_genai import ChatGoogleGenerativeAI
model = ChatGoogleGenerativeAI(
    model="models/gemini-flash-latest", 
    google_api_key=os.getenv("GOOGLE_API_KEY") # 也可以手動指定確保抓到
)

def analyze_sentiment(state: AgentState):
    user_msg = state["messages"][-1].content.lower()
    
    # 簡單的情緒判斷邏輯
    if any(word in user_msg for word in ["高興", "開心", "棒", "good", "happy"]):
        sentiment = "正面"
    elif any(word in user_msg for word in ["生氣", "難過", "差", "bad", "angry"]):
        sentiment = "負面"
    else:
        sentiment = "中性"
    
    print(f"--- 系統日誌：偵測到情緒為 {sentiment} ---")
    # 回傳 sentiment，LangGraph 會自動更新 state
    return {"sentiment": sentiment}

def call_model(state: AgentState):
    # 你甚至可以根據情緒調整 prompt
    sentiment = state.get("sentiment", "未知")
    prompt = f"使用者的情緒是 {sentiment}。請以此心情回應。"
    
    # 將 prompt 放入訊息流中
    response = model.invoke(state["messages"] + [("system", prompt)])
    return {"messages": [response]}