class ExecutorAgent:

    def execute(
        self,
        df,
        query
    ):

        try:

            safe_globals = {
                "df": df
            }

            result = eval(
                query,
                {"__builtins__": {}},
                safe_globals
            )

            return result

        except Exception as e:

            return f"Execution Error: {e}"