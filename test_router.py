from workflow.router_graph import graph
import pandas as pd

df = pd.read_excel(
    "uploads/sample.xlsx"
)

result = graph.invoke(
    {
        "query": "Which author has highest reviews?",
        "dataframe": df
    }
)

print(result)