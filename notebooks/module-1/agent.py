from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

def multiply(a: float, b: float) -> float:
    """
    Multiply a and b.

    Args:
        a: first float
        b: second float
    """
    
    return a * b

def add(a: float, b: float) -> float:
    """
    Adds a and b.

    Args:
        a: first float
        b: second float
    """
    
    return a + b

def divide(a: float, b: float) -> float:
    """
    Divide a and b.

    Args:
        a: first float
        b: second float
    """
    
    return a / b

def subtract(a: float, b: float) -> float:
    """
    Subtract a and b.
    
    Args:
        a: first float
        b: second float
    """
    
    return a - b

def power(a: float, b: float) -> float:
    """
    a to power of b.
    
    Args:
        a: first float
        b: second float
    """
    
    return a ** b

def modulo(a: float, b: float) -> float:
    """
    Remainder of a divide by b.
    
    Args:
        a: first float
        b: second float
    """
    
    return a % b

tools = [add, multiply, divide, subtract, power, modulo]
llm = ChatOpenAI(model="gpt-4.1-mini")
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)

sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

def assistant(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

builder = StateGraph(MessagesState)

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")
graph = builder.compile()
