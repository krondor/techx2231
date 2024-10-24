"""
authors: Elena Lowery and Catherine Cao

This code sample shows how to implement a simple business logic layer for an
AI Assistant application that's running in watsonx.ai
"""

from ibm_watsonx_ai import APIClient

# For invocation of LLM with REST API
import requests, json
from ibm_cloud_sdk_core import IAMTokenManager

def invoke_prompt_template(url,api_key,space_id,deployment_id,task):

    credentials = {
        "url": url,
        "apikey": api_key
    }

    client = APIClient(credentials)
    client.set.default_space(space_id)

    generated_response = client.deployments.generate_text(deployment_id,params={"prompt_variables": {"task": task}})

    print("--------------------------Invocation of a prompt template -------------------------------------------")
    print("Task: " + task)
    print("Response: " + generated_response)
    print("------------------------------------------------------------------------------------------------------")

    return generated_response


def get_auth_token(api_key):

    # Access token is required for REST invocation of the LLM
    access_token = IAMTokenManager(apikey=api_key,url="https://iam.cloud.ibm.com/identity/token").get_token()
    return access_token

def invoke_chat_with_documents(api_key, prompt,endpoint):

    mltoken = get_auth_token(api_key)

    # Chose to retain the history
    retain_history = False
    if (retain_history == False):
        messages = []

    messages.append({"role": "user", "content": prompt})

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": ["Search" "access_token"],
                                       "values": [messages, [mltoken]]}]}


    response_scoring = requests.post(
        endpoint,
        json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})

    print("Scoring response")
    print(response_scoring.json())

    generated_output = response_scoring.json()
    final_output = generated_output['predictions'][0]['values'][1]
    print(final_output)

    return final_output
