import plotly.express as px


class VisualizationAgent:

    def create_charts(self, df):

        charts = []

        numeric_cols = df.select_dtypes(
            include="number"
        ).columns.tolist()

        categorical_cols = df.select_dtypes(
            exclude="number"
        ).columns.tolist()

        # Bar Chart

        if numeric_cols and categorical_cols:

            grouped = (
                df.groupby(categorical_cols[0])[numeric_cols[0]]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )

            fig = px.bar(
                grouped,
                x=categorical_cols[0],
                y=numeric_cols[0],
                title=f"{numeric_cols[0]} by {categorical_cols[0]}"
            )

            charts.append(fig)

        # Histogram

        if numeric_cols:

            fig = px.histogram(
                df,
                x=numeric_cols[0],
                title=f"Distribution of {numeric_cols[0]}"
            )

            charts.append(fig)

        # Correlation Scatter

        if len(numeric_cols) >= 2:

            fig = px.scatter(
                df,
                x=numeric_cols[0],
                y=numeric_cols[1],
                title=f"{numeric_cols[0]} vs {numeric_cols[1]}"
            )

            charts.append(fig)

        return charts