## Introduction: 

This tutorial shows the user how to build and run a simple chatbot that can analyse csv, i.e structured data, using langchain Azure resources. This is a basic use-case demonstrating how an LLM can be used to run analytics on pre-existing csvs. The end-user only needs to upload their file to run the analytics. As a self-contained application, the user does not need to install any libraries, they only need a working browser. 

The repository is based on a tutorial posted on medium by Writers@Tintash. Link: https://medium.com/tintash/talking-to-your-csv-using-openai-and-langchain-aff92c4eb7e2 

The free token provided by OpenAI can be unstable. To circumvent these issues, an Azure resource group was created. 
In this resource group a GPT model was deployed. The specification of this model were:

Type: gpt-4
Deployment type: Standard

*Note: Please ensure that the resource you configure is compatible with the model you would like to build. It would also be prudent to check the model availability in the region you 
choose to build your Azure resource. For more information please check the documentation:* 
https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models?tabs=python-secure%2Cglobal-standard%2Cstandard-chat-completions 

### Data:

The user has the option to upload their own csv and use streamlit_app.py for testing or use the provided Kaggle dataset linked in the docstring in streamlit_app_predictive_maintenance.py. 

*Note: Data must be a csv no greater than 200MB.* 

### Installation:

Use ```pip install -r /path/to/requirements.txt``` to install necessary libraries. 
