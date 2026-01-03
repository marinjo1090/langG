from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # 這個 Annotated 告訴 LangGraph：新的訊息要「附加」上去，而不是「覆蓋」
    messages: Annotated[list[BaseMessage], add_messages]