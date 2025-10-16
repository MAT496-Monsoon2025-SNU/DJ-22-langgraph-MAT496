from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

def gp_sum(a: float, r: float, n: float) -> float:
    """
    Sum of first n terms of a GP with staring term as a and common ratio as r.

    Args:
        a: starting term
        r: common ratio
        n: number of terms
    """
    
    sum = 0
    if r < 1:
        sum = (a * (1 - (r ** n))) / (1 - r)
    elif r > 1:
        sum = (a * ((r ** n) - 1)) / (r - 1)
    else:
        sum = a * n
    
    return sum

def ap_sum(a: float, d: float, n: float) -> float:
    """
    Sum of first n terms of an AP with starting term as a and common differnce as d.
    
    Args:
        a: starting term
        d: common difference
        n: number of terms
    """
    
    sum = (n * 0.5) * ((2 * a) + ((n - 1) * d))
    return sum

llm = ChatOpenAI(model="gpt-4.1-mini")
llm_with_tools = llm.bind_tools([gp_sum, ap_sum])

def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([gp_sum, ap_sum]))
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition,
)
builder.add_edge("tools", END)
graph = builder.compile()