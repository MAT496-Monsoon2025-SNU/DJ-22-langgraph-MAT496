import random 
from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    graph_state: str

def decide_animal(state) -> Literal["node_2", "node_3", "node_4"]:
    if random.random() < 0.33:
        return "node_2"
    elif random.random() < 0.66:
        return "node_3"

    return "node_4"

def node_1(state):
    print("---Node 1---")
    return {"graph_state":state['graph_state'] +" My favourite animal is"}

def node_2(state):
    print("---Node 2---")
    return {"graph_state":state['graph_state'] +" Tiger."}

def node_3(state):
    print("---Node 3---")
    return {"graph_state":state['graph_state'] +" Orca."}

def node_4(state):
    print("---Node 4---")
    return {"graph_state":state['graph_state'] +" Jaguar."}

builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)
builder.add_node("node_4", node_4)
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_animal)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)
builder.add_edge("node_4", END)

graph = builder.compile()