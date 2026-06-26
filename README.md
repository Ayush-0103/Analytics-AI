<div align="center">

# 🚀 Analytics AI

### Enterprise Multi-Agent Analytics Platform

Upload Excel files • AI Analysis • Interactive Dashboards • Executive PPTs • Research Assistant • AI Chat

<img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python">
<img src="https://img.shields.io/badge/LangGraph-Multi--Agent-purple?style=for-the-badge">
<img src="https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit">
<img src="https://img.shields.io/badge/Gemini-AI-green?style=for-the-badge">
<img src="https://img.shields.io/badge/Tavily-Research-orange?style=for-the-badge">

</div>

---

# 📌 Overview

Analytics AI is an enterprise-grade **Multi-Agent Business Analytics Platform** designed to automate the complete analytics workflow for office employees, analysts, consultants, and business teams.

Instead of manually analyzing Excel files and creating reports, users simply upload a dataset and Analytics AI automatically:

* 📊 Performs data analysis
* 🤖 Generates AI-powered business insights
* 📈 Creates interactive visualizations
* 📑 Builds executive PowerPoint presentations
* 🌐 Generates HTML reports
* 🔍 Performs industry research
* 💬 Allows natural language interaction with the dataset
* 🧠 Routes queries intelligently using LangGraph Multi-Agent workflows

---

# ✨ Features

## 📂 Excel Upload

Supports:

* XLSX
* Multiple Sheets
* Automatic Dataset Preview

---

## 📊 Analysis Agent

Automatically detects:

* Dataset Shape
* Column Types
* Numeric Columns
* Categorical Columns
* Missing Values
* KPIs
* Statistical Summary

---

## 🤖 AI Insight Agent

Generates:

* Executive Summary
* Key Business Insights
* Important Observations
* Business Recommendations

Powered by **Google Gemini**

---

## 📈 Visualization Agent

Automatically creates:

* KPI Cards
* Bar Charts
* Pie Charts
* Histograms
* Scatter Plots
* Distribution Analysis

Using **Plotly Interactive Charts**

---

## 📑 PPT Generation Agent

Automatically generates professional presentations containing:

* Title Slide
* Executive Summary
* KPI Summary
* AI Insights
* Business Recommendations
* Interactive Charts
* Professional Formatting

Powered by **python-pptx**

---

## 🌐 HTML Report Generator

Creates client-ready reports including:

* KPI Summary
* Insights
* Charts
* Recommendations

---

## 💬 AI Chat Assistant

Ask questions in natural language such as:

* Which author has highest reviews?
* Show top 5 products.
* Average sales by category.
* Most expensive product.
* Highest rated books.

---

## 🧠 Pandas Agent

Executes analytical operations directly on the uploaded dataframe.

Examples:

* Filtering
* Sorting
* Aggregation
* Grouping
* Statistical Calculations

---

## ⚡ Query Agent

Converts natural language into executable Pandas queries.

Example:

User:

Top 5 books by reviews

↓

Generated Query

↓

Pandas Execution

↓

Result

---

## ⚙ Executor Agent

Safely executes generated Pandas expressions and returns:

* DataFrames
* Lists
* Statistics
* Tables

---

## 🌍 Research Agent

Powered by Tavily API.

Provides:

* Industry Research
* Competitor Analysis
* Market Trends
* Business Benchmarks

---

## 🔀 Router Agent

Automatically decides which AI agent should answer the user's query.

Routes:

* Data Questions
* Research Questions
* General AI Chat

---

## 🔄 LangGraph Workflow

Implements an intelligent Multi-Agent workflow.

```text
User Query
      │
      ▼
 Router Agent
      │
 ┌────┼──────────────┐
 ▼    ▼              ▼
Data Research      Chat
Agent  Agent       Agent
```

---

# 🏗 Architecture

```text
                Upload Excel
                     │
                     ▼
             Analysis Agent
                     │
                     ▼
              Insight Agent
                     │
                     ▼
          Visualization Agent
                     │
      ┌──────────────┴──────────────┐
      ▼                             ▼
 PPT Generator              HTML Report
      │
      ▼
 Executive Presentation
```

---

# 💬 AI Query Flow

```text
User Question
      │
      ▼
 Router Agent
      │
 ┌────┼───────────────┐
 ▼    ▼               ▼
Pandas Research     Chat
Agent  Agent        Agent
      │
      ▼
 Response
```

---

# 🛠 Tech Stack

### Frontend

* Streamlit
* HTML
* CSS

### Backend

* Python

### AI

* Google Gemini
* LangGraph
* Tavily

### Data Processing

* Pandas
* NumPy

### Visualization

* Plotly

### Report Generation

* python-pptx
* HTML

---

# 📁 Project Structure

```text
Analytics AI
│
├── agents
│   ├── analysis_agent.py
│   ├── insight_agent.py
│   ├── visualization_agent.py
│   ├── chat_agent.py
│   ├── pandas_agent.py
│   ├── query_agent.py
│   ├── executor_agent.py
│   ├── router_agent.py
│   ├── research_agent.py
│   ├── ppt_agent.py
│   └── html_report_agent.py
│
├── workflow
│   ├── graph.py
│   ├── router_graph.py
│   └── router_state.py
│
├── pages
│   ├── AI_Chat.py
│   ├── Reports.py
│   ├── Research.py
│   └── Command_Center.py
│
├── uploads
├── reports
├── charts
│
├── app.py
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

Clone the repository

```bash
git clone <repository-url>
```

Navigate into the project

```bash
cd Analytics-AI
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GEMINI_API_KEY=YOUR_GEMINI_KEY
TAVILY_API_KEY=YOUR_TAVILY_KEY
```

Run the application

```bash
streamlit run app.py
```

---

# 📊 Sample Workflow

```text
Upload Excel
      │
      ▼
Automatic Analysis
      │
      ▼
AI Insights
      │
      ▼
Interactive Dashboard
      │
      ▼
Business Charts
      │
      ▼
Executive PPT
      │
      ▼
HTML Report
      │
      ▼
Chat with Dataset
      │
      ▼
Industry Research
```

---

# 🎯 Future Enhancements

* SQL Database Integration
* Multi-file Analytics
* PDF Report Generation
* Scheduled Reports
* Email Automation
* Team Collaboration
* Authentication
* Cloud Deployment
* Voice Assistant
* AI Forecasting
* Predictive Analytics
* RAG Knowledge Base
* Vector Database Integration

---

# 👨‍💻 Author

**Ayush Saxena**

Computer Science Undergraduate

Passionate about AI, Multi-Agent Systems, Data Analytics, and Intelligent Automation.

---

<div align="center">

### ⭐ If you found this project useful, consider giving it a Star!

Built with ❤️ using Python, LangGraph, Gemini & Streamlit.

</div>
