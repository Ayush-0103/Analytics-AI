import pandas as pd


class PandasAgent:

    def execute(
        self,
        df,
        question
    ):

        q = question.lower()

        try:

            # Row Count

            if any(
                phrase in q
                for phrase in [
                    "how many rows",
                    "number of rows",
                    "total rows"
                ]
            ):
                return len(df)

            # Columns

            if "column" in q:
                return df.columns.tolist()

            # Top N Books

            if (
                "top" in q
                and "book" in q
                and "review" in q
            ):

                return (
                    df.nlargest(
                        5,
                        "Reviews"
                    )[
                        [
                            "Name",
                            "Reviews"
                        ]
                    ]
                    .to_dict(
                        "records"
                    )
                )

            # Top Author

            if (
                "author"
                in q
                and (
                    "highest"
                    in q
                    or "top"
                    in q
                )
                and "review"
                in q
            ):

                grouped = (
                    df.groupby(
                        "Author"
                    )[
                        "Reviews"
                    ]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                )

                return grouped.head(
                    5
                ).to_dict()

            # Genre Count

            if (
                "fiction"
                in q
                and "non"
                not in q
            ):

                return len(
                    df[
                        df["Genre"]
                        ==
                        "Fiction"
                    ]
                )

            if (
                "non fiction"
                in q
            ):

                return len(
                    df[
                        df["Genre"]
                        ==
                        "Non Fiction"
                    ]
                )

            # Average Rating

            if (
                "average rating"
                in q
            ):

                return round(
                    df[
                        "User Rating"
                    ].mean(),
                    2
                )

            # Average Price

            if (
                "average price"
                in q
            ):

                return round(
                    df[
                        "Price"
                    ].mean(),
                    2
                )

            # Highest Rated Book

            if (
                "highest rated"
                in q
            ):

                row = df.loc[
                    df[
                        "User Rating"
                    ].idxmax()
                ]

                return {
                    "Book":
                    row["Name"],
                    "Rating":
                    row["User Rating"]
                }

            return None

        except Exception as e:

            return str(e)