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


class QueryAgent:

    def generate_query(
        self,
        columns,
        question
    ):

        prompt = f"""
You are a Pandas expert.

DataFrame name is df.

Columns:
{columns}

Convert the user's question into ONLY a pandas expression.

Examples:

Question:
Top 5 books by reviews

Answer:
df.nlargest(5, "Reviews")[["Name","Reviews"]]

Question:
Average price

Answer:
df["Price"].mean()

Question:
Most expensive book

Answer:
df.loc[df["Price"].idxmax()]

User Question:
{question}

Return ONLY the pandas code.
"""

        response = model.generate_content(
            prompt
        )

        return response.text.strip()