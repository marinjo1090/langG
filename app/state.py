from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # add_messages 會把新訊息 append 到舊清單後
    messages: Annotated[list[BaseMessage], add_messages]