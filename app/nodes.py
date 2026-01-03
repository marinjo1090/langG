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

def call_model(state: AgentState):
    # 讓 AI 根據目前的對話紀錄 (state["messages"]) 產生回應
    response = model.invoke(state["messages"])
    return {"messages": [response]}