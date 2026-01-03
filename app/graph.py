from langgraph.graph import StateGraph, START, END
from .state import AgentState
from .nodes import call_model

workflow = StateGraph(AgentState)

# 增加一個叫 "agent" 的節點，執行 call_model 函式
workflow.add_node("agent", call_model)

# 設定流程：開始 -> agent -> 結束
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

app = workflow.compile()