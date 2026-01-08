from langgraph.graph import StateGraph, START, END
from .state import AgentState
from .nodes import call_model, analyze_sentiment

workflow = StateGraph(AgentState)

# 1. 註冊所有節點
workflow.add_node("sentiment_node", analyze_sentiment)
workflow.add_node("agent", call_model)

# 2. 設定連接線 (Edges)
# 流程變成：開始 -> 情緒分析 -> AI 回答 -> 結束
workflow.add_edge(START, "sentiment_node")
workflow.add_edge("sentiment_node", "agent")
workflow.add_edge("agent", END)


app = workflow.compile()