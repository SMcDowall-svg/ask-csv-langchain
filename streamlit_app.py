import os
import pandas as pd
import streamlit as st
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai.chat_models import AzureChatOpenAI

st.title("Ask your data demo🔍💡")

azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai_api_key = st.sidebar.text_input("Azure OpenAI API Key", type="password") or os.getenv("OPENAI_API_KEY") #not working without directly setting key

if not openai_api_key:
    st.info("Please enter your Azure OpenAI API key in the sidebar to proceed.")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of the uploaded dataset:")
    st.dataframe(df)
else:
    st.warning("Please upload a CSV file to proceed.")

with st.form("my_form"):
    text = st.text_area("Enter text:", "Please type a question.")
    submitted = st.form_submit_button("Submit")

    if submitted:
        if not openai_api_key or not azure_endpoint:
            st.warning("Please enter your Azure OpenAI API key and ensure the endpoint is set!", icon="⚠")
        elif uploaded_file is None:
            st.warning("Please upload a CSV file to enable data processing!", icon="⚠")
        else:
            try:
                llm = AzureChatOpenAI(
                    deployment_name="gpt-4",
                    api_version="2024-08-01-preview",
                    openai_api_key=openai_api_key,
                    azure_endpoint=azure_endpoint,
                    temperature=0,
                    max_tokens=100,
                    timeout=10
                )

                agent_executor = create_pandas_dataframe_agent(
                    llm,
                    df,
                    agent_type="tool-calling",
                    verbose=True,
                    allow_dangerous_code=True
                )

                response = agent_executor.invoke(text)
                try:
                    result_df = pd.DataFrame(eval(response))
                    st.dataframe(result_df)
                except Exception:
                    st.write(response)

            except Exception as e:
                st.error(f"Error: {e}")