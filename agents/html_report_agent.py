import os


class HTMLReportAgent:

    def generate_report(
        self,
        analysis_result,
        insights
    ):

        html = f"""
        <html>

        <head>

        <title>
        Analytics Report
        </title>

        <style>

        body {{
            font-family: Arial;
            margin: 40px;
        }}

        .card {{

            border: 1px solid #ddd;
            padding: 20px;
            margin: 10px;
            border-radius: 10px;

        }}

        </style>

        </head>

        <body>

        <h1>
        Analytics Report
        </h1>

        <div class="card">

        <h2>
        Overview
        </h2>

        <p>
        Rows:
        {analysis_result['rows']}
        </p>

        <p>
        Columns:
        {analysis_result['columns']}
        </p>

        </div>

        <div class="card">

        <h2>
        AI Insights
        </h2>

        <pre>
        {insights}
        </pre>

        </div>

        </body>

        </html>
        """

        os.makedirs(
            "reports",
            exist_ok=True
        )

        path = (
            "reports/report.html"
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(html)

        return path