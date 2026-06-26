from workflow.graph import graph

result = graph.invoke(
    {
        "file_path": "uploads/sample.xlsx"
    }
)

print(result.keys())