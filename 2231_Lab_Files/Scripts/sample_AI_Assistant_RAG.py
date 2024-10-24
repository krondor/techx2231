"""
authors: Elena Lowery and Catherine Cao

This code sample shows how to implement a simple UI for an AI Assistant application that's running in watsonx.ai
"""

# In non-Anaconda Python environments, you may also need to install dotenv
# pip install python-dotenv

# For reading credentials from the .env file
import os
from dotenv import load_dotenv

# All UI capabilities are provided by Streamlit
import streamlit as st

import chat_session
# A Python module that implements calls to LLMs
from watsonx_engine import *
from chat_session import *

# These global variables will be updated in get_credentials() functions
api_key = ""
url = ""
endpoint = ""

def get_credentials():

    load_dotenv()

    # Update the global variables that will be used for authentication in another function
    globals()["api_key"] = os.getenv("api_key", None)
    globals()["url"] = os.getenv("url", None)
    globals()["endpoint"] = os.getenv("endpoint", None)

def main():

    # Retrieve values required for invocation of LLMs from the .env file
    get_credentials()

    # Use the full page instead of a narrow central column
    st.set_page_config(layout="wide")

    # Streamlit UI
    st.title("AI Assistant for 401K questions")
    st.caption("AI Assistant powered by watsonx")

    # Streamlit saves previous messages in a list "messages".
    # Note that this is NOT memory management for LLMs, which needs to be implemented separately
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant",
                                         "content": "I am a technical AI assistant powered by watsonx."}]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # React to user input
    if user_question := st.chat_input('Ask a question, for example: What is IBM?'):
    # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_question)
    
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_question})

        #response = answer_questions(user_question,llm)
        response = generate_response(user_question)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})



def generate_response(prompt):

    response = invoke_chat_with_documents(api_key,prompt,endpoint)

    return response

if __name__ == "__main__":
    main()