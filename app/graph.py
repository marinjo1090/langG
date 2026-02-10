from langgraph.graph import StateGraph, START, END
from .state import AgentState
from .nodes import call_model,tools, reference_check,search_drug_info
from langgraph.prebuilt import ToolNode
import operator

# 定義判斷邏輯：AI 是要「查資料」還是「直接回答」？
def should_continue(state: AgentState):
    # 查詢超過 3 次，強制結束
    if state.get("loop_count", 0) >= 3:
        return "end"
    
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return "end"


workflow = StateGraph(AgentState)

# 1. 加入節點
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools)) # 自動處理工具執行
workflow.add_node("verify", reference_check)

# 2. 設定連線
workflow.add_edge(START, "agent")

# 3. 加入條件分支
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools", # 如果 AI 說要查資料，就去 tools 節點
        "end": END          # 如果 AI 說完話了，就結束
    }
)
# 4. 工具查完後，一定要回到 verify 讓他總結資訊
workflow.add_edge("tools", "verify")
workflow.add_edge("verify", "agent")
app = workflow.compile()