# Groq-Multimodal-Chat

A Streamlit-based front-end for interacting with Groq’s multimodal LLM (Llama 4 Scout) via a simple Python client. Send text and images(both via URL and via Uploading Images from PC) to the model, maintain conversational session history, and display responses in a polished chat UI.

**Prerequisites**
1) Python 3.8 or higher
2) A valid Groq API Key should be stored in a .env file

**Usage**
1) Run the Streamlit app
   ```bash
    streamlit run app_streamlit.py
   ```
    
2) Interact
    * Enter your message and (optionally) an image URL or upload.
    * Click Send to see the model’s response.

4) Streamlit errors
     Upgrade to the latest Streamlit:
    ```bash
     pip install --upgrade streamlit
    ```
