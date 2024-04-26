import streamlit as st
import requests
import sys



# Define the API Gateway URL
API_GW_URL = sys.argv[1]

# Streamlit App
st.title("Mistral 7B Model - Chatbot")

# Input box for user to enter question
question = st.text_input("Enter your question:")

# Button to send question
if st.button("Ask"):
    # Set the headers
    headers = {
        "Content-Type": "application/json"
    }

    # Prepare JSON payload
    payload = {
        "data": {
            "inputs": question,
            "parameters": {
                "do_sample": True,
                "top_p": 0.6,
                "temperature": 0.9,
                "top_k": 50,
                "max_new_tokens": 700,
                "repetition_penalty": 1.03,
                "stop": ["</s>"]
            }
        }
    }
    

    # Send POST request
    response = requests.post(API_GW_URL, headers=headers, json=payload)

    # Display response
    if response.status_code == 200:
        st.success("Response:")
        st.write(response.json())
    else:
        st.error(f"Error: {response.status_code}")
