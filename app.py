import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set page title to match GitHub repo name "CodeFlux"
st.set_page_config(page_title="CodeFlux", layout="wide", initial_sidebar_state="expanded")

# Function to inject CSS directly
def inject_css():
    st.markdown(
        """
        <style>
        /* Gradient background for entire app */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #f0f0f0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        /* Sidebar background with gradient and padding */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #4c51bf 0%, #6b46c1 100%);
            padding-top: 1rem;
            color: white;
        }
        /* Sidebar header styling */
        .sidebar-header {
            text-align: center;
            margin-bottom: 1rem;
        }
        /* Gemini logo styling */
        .gemini-logo {
            width: 120px;
            margin: 0 auto 0.5rem auto;
            display: block;
        }
        /* Sidebar subtitle */
        .sidebar-subtitle {
            font-size: 0.9rem;
            font-weight: 500;
            color: #d6bcfa;
            margin-bottom: 1.5rem;
        }
        /* Chat message bubbles */
        .stChatMessage > div {
            border-radius: 12px !important;
            padding: 0.8rem !important;
            margin-bottom: 0.5rem !important;
            max-width: 80%;
        }
        /* User message bubble */
        .stChatMessage[data-testid="stChatMessage"][data-role="user"] > div {
            background: #9f7aea;
            color: white;
            margin-left: auto;
        }
        /* Assistant message bubble */
        .stChatMessage[data-testid="stChatMessage"][data-role="assistant"] > div {
            background: #6b46c1;
            color: white;
            margin-right: auto;
        }
        /* Code block styling */
        pre {
            background-color: #2d3748 !important;
            border-radius: 8px;
            padding: 1rem !important;
            overflow-x: auto;
        }
        /* Chat input styling */
        div[data-testid="stChatInput"] > div {
            background-color: #5a67d8 !important;
            border-radius: 12px !important;
            color: white !important;
        }
        /* Button styling */
        button[kind="primary"] {
            background: linear-gradient(90deg, #6b46c1 0%, #9f7aea 100%) !important;
            border: none !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.2rem !important;
            border-radius: 12px !important;
            transition: background 0.3s ease;
        }
        button[kind="primary"]:hover {
            background: linear-gradient(90deg, #9f7aea 0%, #6b46c1 100%) !important;
        }
        /* Sidebar toggle button */
        .sidebar-toggle {
            cursor: pointer;
            color: #d6bcfa;
            font-weight: 600;
            margin-bottom: 1rem;
            user-select: none;
            text-align: center;
        }
        /* History container styling */
        .history-container {
            background: rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 1rem;
            max-height: 300px;
            overflow-y: auto;
            margin-bottom: 1rem;
        }
        .history-item {
            border-bottom: 1px solid #9f7aea;
            padding: 0.5rem 0;
        }
        .history-item:last-child {
            border-bottom: none;
        }
        .history-buttons {
            display: flex;
            gap: 0.5rem;
            margin-top: 0.25rem;
        }
        .history-button {
            background: #764ba2;
            border: none;
            color: white;
            padding: 0.3rem 0.6rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.8rem;
            transition: background 0.3s ease;
        }
        .history-button:hover {
            background: #9f7aea;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

inject_css()

# Sidebar toggle state stored in session_state
if "sidebar_visible" not in st.session_state:
    st.session_state.sidebar_visible = True

def toggle_sidebar():
    st.session_state.sidebar_visible = not st.session_state.sidebar_visible

# Sidebar content with Gemini logo and branding
if st.session_state.sidebar_visible:
    with st.sidebar:
        # Sidebar toggle button
        if st.button("⬅️ Hide Sidebar"):
            toggle_sidebar()
        # Gemini logo (using Google Cloud logo as placeholder)
        st.markdown(
            """
            <div class="sidebar-header">
                <img src="https://upload.wikimedia.org/wikipedia/commons/7/7e/Google_Cloud_Logo.svg" alt="Gemini Logo" class="gemini-logo" />
                <div class="sidebar-subtitle">Get started with code powered by Gemini</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        api_key = st.text_input("Enter Gemini API Key:", type="password")
        code_gen_mode = st.checkbox("Enable Code Generation Mode")
        st.markdown("---")
        st.caption("Enter your API key to start chatting")

        # History management section
        st.markdown("### Chat History")
        if "messages" not in st.session_state or len(st.session_state.messages) == 0:
            st.info("No chat history yet.")
        else:
            # Display history with delete buttons
            def delete_message(i):
                st.session_state.messages.pop(i)

            for i, msg in enumerate(st.session_state.messages):
                role = "User" if msg["role"] == "user" else "Assistant"
                with st.expander(f"{role} message #{i+1}", expanded=False):
                    st.write(msg["content"])
                    if st.button(f"Delete message #{i+1}", key=f"del_{i}"):
                        delete_message(i)
                        st.experimental_rerun()

            if st.button("Clear All History"):
                st.session_state.messages = []
                st.experimental_rerun()

else:
    # Minimal sidebar toggle button in main area when sidebar hidden
    if st.button("➡️ Show Sidebar"):
        toggle_sidebar()
    api_key = None
    code_gen_mode = False

# Gemini client initialization
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

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            if code_gen_mode:
                full_prompt = f"Generate code with comments for the following request:\n{prompt}"
            else:
                full_prompt = prompt

            response = model.generate_content(full_prompt)
            text = response.text

            # Properly check for triple backticks inside string
            if "```" in text:
                st.markdown(text)
            else:
                st.write(text)

            st.session_state.messages.append({"role": "assistant", "content": text})
        except Exception as e:
            st.error(f"Error generating response: {e}")

# Footer with credits
st.markdown(
    """
    <div style="text-align:center; margin-top: 2rem; font-size: 0.8rem; color: #d6bcfa;">
        Powered by <b>Gemini</b> & <b>Streamlit</b> | Developed by You
    </div>
    """,
    unsafe_allow_html=True,
)
