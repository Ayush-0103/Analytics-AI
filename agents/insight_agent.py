import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


class InsightAgent:

    def generate_insights(self, analysis_result):

        prompt = f"""
        You are a senior business analyst.

        Analyze the dataset summary below and provide:

        1. Executive Summary
        2. Key Insights
        3. Important Observations

        Dataset Summary:

        {analysis_result}
        """

        response = model.generate_content(prompt)

        return response.text