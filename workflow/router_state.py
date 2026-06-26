from typing import TypedDict, Any


class RouterState(TypedDict):

    query: str

    dataframe: Any

    route: str

    result: Any