import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import datetime
from typing import Dict, List
import time
import re

# Load environment variables
load_dotenv()

# Set page config with custom favicon and layout
st.set_page_config(
    page_title="CodeFlux - AI Code Assistant", 
    page_icon="🚀",
    layout="wide", 
    initial_sidebar_state="expanded"
)

def inject_modern_css():
    """Inject modern, professional CSS styling"""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Root variables for consistent theming */
        :root {
            --primary-bg: #0f0f23;
            --secondary-bg: #1a1a2e;
            --accent-bg: #16213e;
            --primary-text: #ffffff;
            --secondary-text: #a0aec0;
            --accent-color: #00d4ff;
            --success-color: #48bb78;
            --warning-color: #ed8936;
            --error-color: #f56565;
            --border-color: #2d3748;
            --hover-bg: #2d3748;
        }
        
        /* Global app styling */
        .stApp {
            background: linear-gradient(135deg, var(--primary-bg) 0%, var(--secondary-bg) 100%);
            color: var(--primary-text);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom header */
        .app-header {
            background: linear-gradient(90deg, var(--accent-color), #667eea);
            padding: 1rem 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
        }
        
        .app-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            background: linear-gradient(45deg, #ffffff, #e2e8f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .app-subtitle {
            font-size: 1.1rem;
            margin: 0.5rem 0 0 0;
            color: #e2e8f0;
            font-weight: 400;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, var(--secondary-bg) 0%, var(--accent-bg) 100%);
            border-right: 1px solid var(--border-color);
        }
        
        .sidebar-section {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid var(--border-color);
            backdrop-filter: blur(10px);
        }
        
        .section-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--accent-color);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        /* Chat message styling */
        .stChatMessage {
            margin-bottom: 1rem !important;
        }
        
        .stChatMessage > div {
            border-radius: 16px !important;
            padding: 1.2rem !important;
            margin-bottom: 0.8rem !important;
            max-width: 85% !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
        }
        
        /* User message */
        .stChatMessage[data-testid="stChatMessage"][data-role="user"] > div {
            background: linear-gradient(135deg, var(--accent-color), #667eea) !important;
            color: white !important;
            margin-left: auto !important;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Assistant message */
        .stChatMessage[data-testid="stChatMessage"][data-role="assistant"] > div {
            background: linear-gradient(135deg, var(--accent-bg), var(--secondary-bg)) !important;
            color: var(--primary-text) !important;
            margin-right: auto !important;
            border: 1px solid var(--border-color);
        }
        
        /* Code blocks */
        pre {
            background: linear-gradient(135deg, #1a202c, #2d3748) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            overflow-x: auto !important;
            font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
        
        code {
            background: rgba(0, 212, 255, 0.1) !important;
            color: var(--accent-color) !important;
            padding: 0.2rem 0.4rem !important;
            border-radius: 4px !important;
            font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
        }
        
        /* Input styling */
        .stChatInput > div {
            background: linear-gradient(90deg, var(--secondary-bg), var(--accent-bg)) !important;
            border-radius: 24px !important;
            border: 1px solid var(--border-color) !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        
        .stChatInput input {
            background: transparent !important;
            color: var(--primary-text) !important;
            border: none !important;
            font-size: 1rem !important;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(90deg, var(--accent-color), #667eea) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0, 212, 255, 0.4) !important;
        }
        
        /* Text input styling */
        .stTextInput > div > div > input {
            background: var(--secondary-bg) !important;
            color: var(--primary-text) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
        }
        
        /* Select box styling */
        .stSelectbox > div > div {
            background: var(--secondary-bg) !important;
            color: var(--primary-text) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
        }
        
        /* Metrics styling */
        [data-testid="metric-container"] {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            backdrop-filter: blur(10px);
        }
        
        /* Success/info/warning/error messages */
        .stSuccess, .stInfo, .stWarning, .stError {
            border-radius: 12px !important;
            backdrop-filter: blur(10px) !important;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.05) !important;
            border-radius: 8px !important;
            border: 1px solid var(--border-color) !important;
        }
        
        /* History item styling */
        .history-item {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 8px;
            padding: 0.8rem;
            margin-bottom: 0.5rem;
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
        }
        
        .history-item:hover {
            background: rgba(255, 255, 255, 0.08);
            transform: translateX(4px);
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--secondary-bg);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--accent-color);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #0099cc;
        }
        
        /* Animation for loading */
        @keyframes pulse {
            0% { opacity: 0.6; }
            50% { opacity: 1; }
            100% { opacity: 0.6; }
        }
        
        .loading {
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        /* Stats container */
        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .stat-card {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(102, 126, 234, 0.1));
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        
        .stat-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--accent-color);
        }
        
        .stat-label {
            font-size: 0.8rem;
            color: var(--secondary-text);
            margin-top: 0.25rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def create_app_header():
    """Create a modern app header"""
    st.markdown(
        """
        <div class="app-header">
            <h1 class="app-title">🚀 CodeFlux</h1>
            <p class="app-subtitle">AI-Powered Code Assistant with Gemini</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        "messages": [],
        "total_tokens": 0,
        "session_start": datetime.datetime.now(),
        "message_count": 0,
        "current_model": "gemini-2.0-flash",
        "conversation_title": "New Conversation",
        "saved_conversations": {},
        "current_conversation_id": None,
        "user_preferences": {
            "code_theme": "dark",
            "response_style": "balanced",
            "auto_save": True
        }
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def save_conversation():
    """Save current conversation"""
    if not st.session_state.messages:
        return
    
    conv_id = st.session_state.current_conversation_id or str(int(time.time()))
    st.session_state.saved_conversations[conv_id] = {
        "title": st.session_state.conversation_title,
        "messages": st.session_state.messages.copy(),
        "timestamp": datetime.datetime.now().isoformat(),
        "message_count": len(st.session_state.messages)
    }
    st.session_state.current_conversation_id = conv_id

def load_conversation(conv_id):
    """Load a saved conversation"""
    if conv_id in st.session_state.saved_conversations:
        conv = st.session_state.saved_conversations[conv_id]
        st.session_state.messages = conv["messages"]
        st.session_state.conversation_title = conv["title"]
        st.session_state.current_conversation_id = conv_id
        st.rerun()

def export_conversation():
    """Export conversation to JSON"""
    if not st.session_state.messages:
        return None
    
    export_data = {
        "title": st.session_state.conversation_title,
        "timestamp": datetime.datetime.now().isoformat(),
        "messages": st.session_state.messages,
        "stats": {
            "message_count": len(st.session_state.messages),
            "session_duration": str(datetime.datetime.now() - st.session_state.session_start)
        }
    }
    
    return json.dumps(export_data, indent=2)

def create_sidebar():
    """Create enhanced sidebar with multiple sections"""
    with st.sidebar:
        # API Configuration Section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔧 Configuration</div>', unsafe_allow_html=True)
        
        api_key = st.text_input(
            "Gemini API Key:",
            type="password",
            help="Enter your Google Gemini API key"
        )
        
        model_options = [
            "gemini-2.0-flash",
            "gemini-1.5-pro",
            "gemini-1.5-flash"
        ]
        selected_model = st.selectbox(
            "Model:",
            model_options,
            index=model_options.index(st.session_state.current_model)
        )
        st.session_state.current_model = selected_model
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Features Section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚡ Features</div>', unsafe_allow_html=True)
        
        code_gen_mode = st.checkbox("🔨 Code Generation Mode", help="Optimized for code generation")
        explain_mode = st.checkbox("📚 Explanation Mode", help="Detailed explanations")
        debug_mode = st.checkbox("🐛 Debug Mode", help="Help debug code issues")
        
        response_style = st.radio(
            "Response Style:",
            ["Concise", "Balanced", "Detailed"],
            index=1
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Statistics Section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Session Stats</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Messages", len(st.session_state.messages))
        with col2:
            duration = datetime.datetime.now() - st.session_state.session_start
            st.metric("Duration", f"{duration.seconds//60}m")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Conversation Management
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">💾 Conversations</div>', unsafe_allow_html=True)
        
        conv_title = st.text_input(
            "Conversation Title:",
            value=st.session_state.conversation_title,
            max_chars=50
        )
        st.session_state.conversation_title = conv_title
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save", use_container_width=True):
                save_conversation()
                st.success("Saved!")
        
        with col2:
            if st.button("🆕 New", use_container_width=True):
                if st.session_state.user_preferences["auto_save"] and st.session_state.messages:
                    save_conversation()
                st.session_state.messages = []
                st.session_state.current_conversation_id = None
                st.session_state.conversation_title = "New Conversation"
                st.rerun()
        
        # Saved Conversations
        if st.session_state.saved_conversations:
            st.markdown("**Saved Conversations:**")
            for conv_id, conv in st.session_state.saved_conversations.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button(
                        f"📄 {conv['title'][:20]}..." if len(conv['title']) > 20 else f"📄 {conv['title']}",
                        key=f"load_{conv_id}",
                        use_container_width=True
                    ):
                        load_conversation(conv_id)
                with col2:
                    if st.button("🗑️", key=f"del_{conv_id}"):
                        del st.session_state.saved_conversations[conv_id]
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export Section
        if st.session_state.messages:
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📤 Export</div>', unsafe_allow_html=True)
            
            export_data = export_conversation()
            if export_data:
                st.download_button(
                    label="📁 Download JSON",
                    data=export_data,
                    file_name=f"codeflux_conversation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    return api_key, code_gen_mode, explain_mode, debug_mode, response_style

def format_response_with_mode(prompt: str, code_gen_mode: bool, explain_mode: bool, debug_mode: bool, response_style: str) -> str:
    """Format the prompt based on selected modes"""
    prefix_parts = []
    
    if code_gen_mode:
        prefix_parts.append("Generate clean, well-commented code")
    
    if explain_mode:
        prefix_parts.append("Provide detailed explanations")
    
    if debug_mode:
        prefix_parts.append("Help debug and identify issues")
    
    style_instructions = {
        "Concise": "Keep responses brief and to the point",
        "Balanced": "Provide moderate detail with good examples",
        "Detailed": "Give comprehensive explanations with multiple examples"
    }
    
    prefix_parts.append(style_instructions[response_style])
    
    if prefix_parts:
        return f"{'. '.join(prefix_parts)}.\n\nUser request: {prompt}"
    
    return prompt

def display_chat_message(message: Dict[str, str], message_index: int):
    """Display a chat message with enhanced formatting"""
    with st.chat_message(message["role"]):
        content = message["content"]
        
        # Check if message contains code blocks
        if "```" in content:
            st.markdown(content)
        else:
            st.write(content)
        
        # Add message actions
        if message["role"] == "assistant":
            col1, col2, col3, col4 = st.columns([1, 1, 1, 6])
            
            with col1:
                if st.button("👍", key=f"like_{message_index}", help="Like this response"):
                    st.toast("Response liked! 👍")
            
            with col2:
                if st.button("👎", key=f"dislike_{message_index}", help="Dislike this response"):
                    st.toast("Feedback noted 👎")
            
            with col3:
                if st.button("📋", key=f"copy_{message_index}", help="Copy to clipboard"):
                    st.toast("Copied to clipboard! 📋")

def main():
    """Main application function"""
    # Initialize
    inject_modern_css()
    initialize_session_state()
    create_app_header()
    
    # Create sidebar and get settings
    api_key, code_gen_mode, explain_mode, debug_mode, response_style = create_sidebar()
    
    # Initialize Gemini
    effective_api_key = api_key or os.getenv("GOOGLE_API_KEY")
    if not effective_api_key:
        st.error("🔑 Please enter your Gemini API key in the sidebar to continue.")
        st.info("""
        **How to get your API key:**
        1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Create a new API key
        3. Copy and paste it in the sidebar
        """)
        st.stop()
    
    try:
        genai.configure(api_key=effective_api_key)
        model = genai.GenerativeModel(st.session_state.current_model)
    except Exception as e:
        st.error(f"❌ Error initializing Gemini model: {e}")
        st.stop()
    
    # Display chat messages
    for i, message in enumerate(st.session_state.messages):
        display_chat_message(message, i)
    
    # Chat input and processing
    if prompt := st.chat_input("💬 Ask me anything about code..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    # Format prompt based on modes
                    formatted_prompt = format_response_with_mode(
                        prompt, code_gen_mode, explain_mode, debug_mode, response_style
                    )
                    
                    # Generate response
                    response = model.generate_content(formatted_prompt)
                    response_text = response.text
                    
                    # Display response
                    if "```" in response_text:
                        st.markdown(response_text)
                    else:
                        st.write(response_text)
                    
                    # Add to message history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response_text
                    })
                    
                    # Auto-save if enabled
                    if st.session_state.user_preferences["auto_save"]:
                        save_conversation()
                    
                except Exception as e:
                    st.error(f"❌ Error generating response: {e}")
                    st.info("Please check your API key and try again.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; padding: 1rem; color: #a0aec0; font-size: 0.9rem;">
            <strong>CodeFlux</strong> - Powered by <strong>Gemini AI</strong> & <strong>Streamlit</strong><br>
            Built with ❤️ for developers by developers
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
