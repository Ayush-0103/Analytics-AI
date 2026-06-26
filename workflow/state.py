
from typing import TypedDict


class WorkflowState(TypedDict):

    file_path: str

    analysis_result: dict

    insights: str

    charts: list

    chart_paths: list

    ppt_path: str