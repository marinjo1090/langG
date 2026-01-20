import os
from dotenv import load_dotenv
from .state import AgentState

load_dotenv() # 自動抓取 .env 裡面的 KEY
from langchain_google_genai import ChatGoogleGenerativeAI
model = ChatGoogleGenerativeAI(
    model="models/gemini-flash-latest", 
    google_api_key=os.getenv("GOOGLE_API_KEY") # 也可以手動指定確保抓到
)

from langchain_community.tools.tavily_search import TavilyAnswer
from langchain_core.tools import tool

# 定義一個專門查藥物禁忌的工具
@tool
def search_drug_info(query: str):
    """
    當需要查詢藥品成分、藥物禁忌或藥物與食物的交互作用時，使用此工具。
    輸入應該是具體的藥名或問題，例如「阿斯匹靈 禁忌」。
    """
    from langchain_community.tools.tavily_search import TavilySearchResults
    search = TavilySearchResults(max_results=2) # 抓取最相關的 2 則資料
    return search.invoke(query)

# 綁定工具到模型
tools = [search_drug_info]
model_with_tools = model.bind_tools(tools)

# 修改 call_model 節點
def call_model(state: AgentState):
    # 讓模型決定是否要用搜尋工具
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}