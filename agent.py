from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import requests
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


def main():
    load_dotenv()
    st.set_page_config(page_title="Ask your Dataset")

    st.header("Ask your Dataset 💬")

    # Upload file
    file = st.file_uploader("Upload your File", type="csv")

    # Initialize OpenAI LLM
    llm = OpenAI()

    # Define a LangChain prompt template for the LLM to extract info
    prompt_template = PromptTemplate(
        input_variables=["entity", "snippets", "user_query"],
        template="Extract the information specified in '{user_query}' for '{entity}' from the following text snippets:\n{snippets}"
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt_template)

    if file is not None:
        df = pd.read_csv(file)
        st.write(df)

        # Select a column to use for placeholder replacement
        selected_column = st.selectbox("Select a column to use as placeholder values:", options=df.columns)
        user_prompt = st.text_input(
            "Enter your custom prompt with placeholders (e.g., 'Get the email address of {placeholder}'):")

        if user_prompt and selected_column:
            search_results = []
            for _, row in df.iterrows():
                entity = row[selected_column]
                query = user_prompt.replace("{placeholder}", str(entity))

                # Perform web search
                search_snippets = search_entity(query)
                snippets_text = " ".join([result["snippet"] for result in search_snippets])

                # Print the entity name
                st.subheader(f"{entity}")

                # Display the search snippets
                for result in search_snippets:
                    st.write(f"- **Link**: {result['link']}")
                    st.write(f"  **Snippet**: {result['snippet']}")

                # Use LLM to extract information from snippets
                if snippets_text:
                    extracted_info = llm_chain.run(entity=entity, snippets=snippets_text, user_query=user_prompt)
                    search_results.append({"entity": entity, "extracted_info": extracted_info})

                    # Display the extracted information
                    st.write("**Extracted Information:**")
                    st.write(extracted_info)

            # Store results in a DataFrame for further processing or download
            extracted_df = pd.DataFrame(search_results)
            st.session_state["extracted_data"] = extracted_df


def search_entity(query):
    SERP_API_KEY = os.getenv("SERP_API")
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "engine": "google",
        "num": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Extract URLs and snippets from results
    results = []
    for result in data.get("organic_results", []):
        results.append({
            "link": result.get("link"),
            "snippet": result.get("snippet")
        })

    return results


if __name__ == '__main__':
    main()
