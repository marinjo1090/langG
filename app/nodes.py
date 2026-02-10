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
    當問題提及藥物相關資訊或禁忌時使用此工具，提及藥物的通俗名稱也應使用，如止痛、鐵牛運功散、大正百保能等
    藥物安全搜尋工具。專門查詢台灣官方藥典、大型醫院與學術機構資料。
    當查詢到的資料不構可靠或是不足以準確地回答問題時，請再次使用此工具進行補充查詢。
    """
    from langchain_community.tools.tavily_search import TavilySearchResults
    
    # 限定搜尋範圍，避免內容農場（如：每日頭條、隨便的部落格）
    search = TavilySearchResults(
        max_results=3,
        # 你可以加入台灣權威的醫療網域
        include_domains=[
            "fda.gov.tw",      # 食藥署
            "nhi.gov.tw",      # 健保署
            "mohw.gov.tw",     # 衛福部
            "cgmh.org.tw",     # 長庚醫院
            "ntuh.gov.tw",     # 台大醫院
            "vghtpe.gov.tw"    # 台北榮總
        ]
    )
    return search.invoke(query)

from langchain_core.messages import SystemMessage, HumanMessage

def reference_check(state: AgentState):
    # 1. 取得最新訊息 (ToolMessage)
    last_msg = state["messages"][-1]
    content = str(last_msg.content)
    user_query = state["messages"][0].content # 最初的問題

    # --- 階段一：硬性規則檢查 (節省 Token) ---
    if not content or len(content) < 50:
        return {
            "messages": [SystemMessage(content="系統提示：搜尋結果過短或無內容。")],
            "loop_count": 1
        }

    # --- 階段二：醫療關鍵字過濾 ---
    med_keywords = ["藥", "交互作用", "副作用", "用法", "禁忌", "醫師", "臨床"]
    relevance_hits = sum(1 for word in med_keywords if word in content)
    if relevance_hits < 1:
        return {
            "messages": [SystemMessage(content="系統提示：搜尋結果與醫療藥物無關。")],
            "loop_count": 1
        }

    # --- 階段三：LLM 語意相關性驗證 (小腦驗證) ---
    check_prompt = f"""
    請判斷搜尋結果是否與用戶問題相關，並能提供藥物安全性建議？
    用戶問題：{user_query}
    搜尋結果片段：{content[:800]}
    
    只需回答「是」或「否」。
    """
    # 呼叫模型進行評分 (Grading)
    grade = model.invoke([HumanMessage(content=check_prompt)]).content
    
    if "否" in grade:
        return {
            "messages": [SystemMessage(content="系統提示：搜尋結果無法回答用戶具體要求的藥物交互作用。請重新嘗試更精確的搜尋。")],
            "loop_count": 1
        }

    # --- 階段四：來源可信度標記 ---
    official_domains = ["gov.tw", "org.tw", "edu.tw"]
    is_official = any(domain in content for domain in official_domains)
    
    if not is_official:
        return {
            "messages": [SystemMessage(content="系統提示：來源非官方。回答時請務必提醒用戶此資訊僅供參考，應諮詢醫師。")],
            "loop_count": 1
        }

    return {"messages": [SystemMessage(content="OK喲。")], "loop_count": 1}

# 綁定工具到模型
tools = [search_drug_info]
model_with_tools = model.bind_tools(tools)

# 修改 call_model 節點
def call_model(state: AgentState):
    # 讓模型決定是否要用搜尋工具
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}

