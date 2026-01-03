import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from .state import AgentState

import os
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# 1. 定義一個工具
@tool
def multiply(a: int, b: int) -> int:
    """將兩個整數相乘。"""
    return a * b

tools = [multiply]

# 2. 建立模型並「綁定」工具
model = ChatGoogleGenerativeAI(
    model="models/gemini-flash-latest",
    google_api_key=os.getenv("GOOGLE_API_KEY")
).bind_tools(tools) # 重要：這讓 AI 知道有這個工具可用

def call_model(state):
    response = model.invoke(state["messages"])
    return {"messages": [response]}