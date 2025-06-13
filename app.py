# app.py
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure app layout
st.set_page_config(page_title="Gemini Chatbot", layout="wide")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    code_generation_mode = st.checkbox("Enable Code Generation Mode")
    st.markdown("---")
    st.caption("Enter your API key and toggle code generation mode as needed")

# Initialize Gemini client
if api_key or os.getenv("GOOGLE_API_KEY"):
    try:
        genai.configure(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"Error initializing Gemini: {e}")
else:
    st.info("Please enter your Gemini API key in the sidebar to start chatting")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input and processing
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        try:
            if code_generation_mode:
                response = model.generate_content(
                    f"Generate code for: {prompt}. Provide implementation with comments."
                )
            else:
                response = model.generate_content(prompt)
            
            # Display response with code formatting
            if "```
                st.markdown(response.text)
            else:
                st.write(response.text)
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error generating response: {e}")
