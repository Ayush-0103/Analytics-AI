from langgraph.graph import StateGraph, END

from workflow.state import WorkflowState

from agents.analysis_agent import AnalysisAgent
from agents.insight_agent import InsightAgent
from agents.visualization_agent import VisualizationAgent
from agents.ppt_agent import PPTAgent

import os


analysis_agent = AnalysisAgent()
insight_agent = InsightAgent()
visualization_agent = VisualizationAgent()
ppt_agent = PPTAgent()
def analysis_node(state):

    result = analysis_agent.analyze(
        state["file_path"]
    )

    state["analysis_result"] = result

    return state
def insight_node(state):

    insights = insight_agent.generate_insights(
        state["analysis_result"]
    )

    state["insights"] = insights

    return state    
def visualization_node(state):

    charts = visualization_agent.create_charts(
        state["analysis_result"]["dataframe"]
    )

    os.makedirs(
        "graphs",
        exist_ok=True
    )

    chart_paths = []

    for i, chart in enumerate(charts):

        chart_path = f"graphs/chart_{i}.png"

        chart.write_image(chart_path)

        chart_paths.append(chart_path)

    state["charts"] = charts
    state["chart_paths"] = chart_paths

    return state
def ppt_node(state):

    ppt_path = ppt_agent.generate_ppt(
        state["analysis_result"],
        state["insights"],
        state["chart_paths"]
    )

    state["ppt_path"] = ppt_path

    return state
builder = StateGraph(
    WorkflowState
)

builder.add_node(
    "analysis",
    analysis_node
)

builder.add_node(
    "insights",
    insight_node
)

builder.add_node(
    "visualization",
    visualization_node
)

builder.add_node(
    "ppt",
    ppt_node
)

builder.set_entry_point(
    "analysis"
)

builder.add_edge(
    "analysis",
    "insights"
)

builder.add_edge(
    "insights",
    "visualization"
)

builder.add_edge(
    "visualization",
    "ppt"
)

builder.add_edge(
    "ppt",
    END
)

graph = builder.compile()