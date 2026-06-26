class RouterAgent:

    def route(
        self,
        query
    ):

        q = query.lower()

        research_keywords = [
            "industry",
            "market",
            "competitor",
            "trend",
            "research",
            "benchmark"
        ]

        report_keywords = [
            "ppt",
            "presentation",
            "report",
            "download"
        ]

        data_keywords = [
            "top",
            "average",
            "highest",
            "lowest",
            "count",
            "show",
            "how many"
        ]

        if any(
            word in q
            for word in research_keywords
        ):
            return "research"

        if any(
            word in q
            for word in report_keywords
        ):
            return "report"

        if any(
            word in q
            for word in data_keywords
        ):
            return "data"

        return "chat"