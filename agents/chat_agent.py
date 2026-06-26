import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


class ChatAgent:

    def ask(
        self,
        dataframe,
        question
    ):

        context = f"""
        Dataset Columns:
        {dataframe.columns.tolist()}

        Dataset Summary:
        {dataframe.describe(include='all').to_string()}

        Sample Data:
        {dataframe.head(10).to_string()}

        User Question:
        {question}

        Answer only using the dataset provided.
        If the information is not available in the dataset,
        say so clearly.
        """

        try:

            response = model.generate_content(
                context
            )

            return response.text

        except Exception as e:

            return f"Error: {str(e)}"