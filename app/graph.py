from langgraph.graph import StateGraph, START, END
from .state import AgentState
from .nodes import call_model,tools
from langgraph.prebuilt import ToolNode
import operator


# 定義判斷邏輯：AI 是要「查資料」還是「直接回答」？
def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow = StateGraph(AgentState)

# 1. 加入節點
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools)) # 自動處理工具執行

# 2. 設定連線
workflow.add_edge(START, "agent")

# 3. 加入條件分支
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools", # 如果 AI 說要查資料，就去 tools 節點
        END: END          # 如果 AI 說完話了，就結束
    }
)

# 4. 工具查完後，一定要回到 agent 讓他總結資訊
workflow.add_edge("tools", "agent")

app = workflow.compile()