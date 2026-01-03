
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from app.state import AgentState
from app.nodes import call_model, tools # 匯入我們剛寫的東西

workflow = StateGraph(AgentState)

# 1. 加入 Agent 節點
workflow.add_node("agent", call_model)

# 2. 加入工具執行節點 (這是 LangGraph 內建的方便功能)
tool_node = ToolNode(tools)
workflow.add_node("tools", tool_node)

# 3. 設定邏輯：
workflow.add_edge(START, "agent")

# 4. 關鍵：條件式連線 (Conditional Edge)
# 如果 agent 決定要用工具，就去 tools；否則就結束 END
workflow.add_conditional_edges(
    "agent",
    tools_condition, 
)

# 5. 工具執行完後，一定要回到 agent 讓它總結答案
workflow.add_edge("tools", "agent")

app = workflow.compile()