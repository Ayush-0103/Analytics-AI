import pandas as pd


class AnalysisAgent:

    def analyze(self, file_path):

        excel_file = pd.ExcelFile(file_path)

        sheet_names = excel_file.sheet_names

        df = pd.read_excel(
            file_path,
            sheet_name=sheet_names[0]
        )

        numeric_cols = df.select_dtypes(
            include="number"
        ).columns.tolist()

        categorical_cols = df.select_dtypes(
            exclude="number"
        ).columns.tolist()

        kpis = {}

        for col in numeric_cols:
            kpis[col] = {
                "sum": float(round(df[col].sum(), 2)),
                "mean": float(round(df[col].mean(), 2)),
                "max": float(df[col].max()),
                "min": float(df[col].min())
            }

        missing_values = df.isnull().sum().to_dict()

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "sheet_names": sheet_names,
            "column_names": df.columns.tolist(),
            "numeric_columns": numeric_cols,
            "categorical_columns": categorical_cols,
            "kpis": kpis,
            "missing_values": missing_values,
            "preview": df.head().to_dict("records"),
            "dataframe": df
        }