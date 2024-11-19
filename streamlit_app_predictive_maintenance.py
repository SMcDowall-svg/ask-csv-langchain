import os
import pandas as pd
import streamlit as st
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai.chat_models import AzureChatOpenAI

st.title("Ask your data demo🔍💡")
st.subheader("This app aims to demonstrate a simple chatbot with langchain using Azure resources.")
st.write("""
### About Dataset

**Source**: [Kaggle - Machine Predictive Maintenance Classification](https://www.kaggle.com/datasets/shivamb/machine-predictive-maintenance-classification)  

**Machine Predictive Maintenance Classification Dataset**  
Since real predictive maintenance datasets are generally difficult to obtain and in particular difficult to publish, we present and provide a synthetic dataset that reflects real predictive maintenance encountered in the industry to the best of our knowledge.  

The dataset consists of 10,000 data points stored as rows with 14 features in columns:  
- **UID**: unique identifier ranging from 1 to 10,000  
- **productID**: consisting of a letter L, M, or H for low (50% of all products), medium (30%), and high (20%) as product quality variants and a variant-specific serial number  
- **air temperature [K]**: generated using a random walk process later normalized to a standard deviation of 2 K around 300 K  
- **process temperature [K]**: generated using a random walk process normalized to a standard deviation of 1 K, added to the air temperature plus 10 K.  
- **rotational speed [rpm]**: calculated from power of 2860 W, overlaid with a normally distributed noise  
- **torque [Nm]**: torque values are normally distributed around 40 Nm with an σ = 10 Nm and no negative values.  
- **tool wear [min]**: The quality variants H/M/L add 5/3/2 minutes of tool wear to the used tool in the process.  
- **machine failure**: A label that indicates whether the machine has failed in this particular data point for any of the following failure modes.  

**Important**: There are two Targets - Do not make the mistake of using one of them as a feature, as it will lead to leakage:  
- **Target**: Failure or Not  
- **Failure Type**: Type of Failure  
""")

azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai_api_key = st.sidebar.text_input("Azure OpenAI API Key", type="password") or os.getenv("OPENAI_API_KEY") #alternative to use own key stored locally

if not openai_api_key:
    st.info("Please enter your Azure OpenAI API key in the sidebar to proceed.")
    
df = pd.read_csv('data/predictive_maintenance.csv')

with st.form("my_form"):
    text = st.text_area("Enter text:", "Please type a question.")
    submitted = st.form_submit_button("Submit")

    if submitted:
        if not openai_api_key or not azure_endpoint:
            st.warning("Please enter your Azure OpenAI API key and ensure the endpoint is set!", icon="⚠")
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