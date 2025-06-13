import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env (optional)
load_dotenv()

st.set_page_config(page_title="Gemini Chatbot", layout="wide")

# Sidebar for API key and options
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    code_gen_mode = st.checkbox("Enable Code Generation Mode")
    st.markdown("---")
    st.caption("Enter your API key to start chatting")

# Initialize Gemini client if API key is provided
if api_key or os.getenv("GOOGLE_API_KEY"):
    try:
        genai.configure(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        st.error(f"Error initializing Gemini model: {e}")
        st.stop()
else:
    st.info("Please enter your Gemini API key in the sidebar to start chatting")
    st.stop()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        try:
            # Prepare prompt for code generation if enabled
            if code_gen_mode:
                full_prompt = f"Generate code for the following request with explanations:\n{prompt}"
            else:
                full_prompt = prompt

            response = model.generate_content(full_prompt)

            # Extract text from response
            text = response.text

            # Detect if response contains code block markdown
            if "```" in text:
                st.markdown(text)
            else:
                st.write(text)

            # Append assistant message to history
            st.session_state.messages.append({"role": "assistant", "content": text})

        except Exception as e:
            st.error(f"Error generating response: {e}")
