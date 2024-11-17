# AI_agent_for_dataset

## Description:
Created an interactive Streamlit application that leverages OpenAI's Language Learning Models (LLMs) via LangChain to enable users to query their datasets with natural language prompts. It integrates the SERP API for real-time web searches to enhance dataset analysis by fetching and extracting relevant information from the internet.

## Setup Instructions:
- Clone the repository: git clone https://github.com/your-repo/ask-your-dataset.git
- Install dependencies: pip install -r requirements.txt
- Create a .env file from .env.example and fill in the API key.
- Run the app: streamlit run agent.py

## Usage Guide:
- Upload a CSV.
- Select a column for placeholders.
- Enter a custom prompt

## Third-Party Tools:
- LangChain: For LLM integration.
- SERP API: For web search.
- OpenAI API: For LLM capabilities.
