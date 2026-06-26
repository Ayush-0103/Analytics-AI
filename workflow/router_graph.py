from langgraph.graph import StateGraph, END

from workflow.router_state import RouterState

from agents.router_agent import RouterAgent
from agents.pandas_agent import PandasAgent
from agents.research_agent import ResearchAgent
from agents.chat_agent import ChatAgent


# =====================================
# Agent Initialization
# =====================================

router_agent = RouterAgent()
pandas_agent = PandasAgent()
research_agent = ResearchAgent()
chat_agent = ChatAgent()


# =====================================
# Router Node
# =====================================

def router_node(state):

    route = router_agent.route(
        state["query"]
    )

    state["route"] = route

    return state


# =====================================
# Data Node
# =====================================

def data_node(state):

    result = pandas_agent.execute(
        state["dataframe"],
        state["query"]
    )

    state["result"] = result

    return state


# =====================================
# Research Node
# =====================================

def research_node(state):

    result = research_agent.research(
        state["query"]
    )

    state["result"] = result

    return state


# =====================================
# Chat Node
# =====================================

def chat_node(state):

    result = chat_agent.ask(
        state["dataframe"],
        state["query"]
    )

    state["result"] = result

    return state


# =====================================
# Route Decision
# =====================================

def decide_route(state):

    return state["route"]


# =====================================
# Build LangGraph
# =====================================

builder = StateGraph(
    RouterState
)

builder.add_node(
    "router",
    router_node
)

builder.add_node(
    "data",
    data_node
)

builder.add_node(
    "research",
    research_node
)

builder.add_node(
    "chat",
    chat_node
)

builder.set_entry_point(
    "router"
)

builder.add_conditional_edges(
    "router",
    decide_route,
    {
        "data": "data",
        "research": "research",
        "chat": "chat"
    }
)

builder.add_edge(
    "data",
    END
)

builder.add_edge(
    "research",
    END
)

builder.add_edge(
    "chat",
    END
)

graph = builder.compile()