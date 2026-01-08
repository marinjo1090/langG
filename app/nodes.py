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

from langchain_core.messages import SystemMessage, HumanMessage

def analyze_sentiment(state: AgentState):
    user_msg = state["messages"][-1].content  # 取得使用者最後一句話
    
    # 建立一個專門分析情緒的 Prompt
    prompt = [
        SystemMessage(content="你是一個情緒分析專家。請分析使用者的輸入，只回傳：'正面'、'負面' 或 '中性'。不要解釋，只要這兩個字。"),
        HumanMessage(content=user_msg)
    ]
    
    # 使用你定義好的 model (例如 ChatOpenAI 或 ChatGoogleGenerativeAI)
    response = model.invoke(prompt)
    sentiment = response.content.strip()
    
    print(f"--- 系統日誌：LLM 判定情緒為 {sentiment} ---")
    return {"sentiment": sentiment}

def call_model(state: AgentState):
    # 你甚至可以根據情緒調整 prompt
    sentiment = state.get("sentiment", "未知")
    prompt = f"使用者的情緒是 {sentiment}。請以此心情回應。"
    
    # 將 prompt 放入訊息流中
    response = model.invoke(state["messages"] + [("system", prompt)])
    return {"messages": [response]}