import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import datetime
from typing import Dict, List
import time
import re
import base64

# Load environment variables
load_dotenv()

# Set page config with custom favicon and layout
st.set_page_config(
    page_title="FluxCode - AI Code Assistant", 
    page_icon="🚀",
    layout="wide", 
    initial_sidebar_state="expanded"
)

def create_logo_svg():
    """Create the FluxCode logo as SVG"""
    return """
    <svg width="120" height="120" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#00d4ff;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#0099cc;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#667eea;stop-opacity:1" />
            </linearGradient>
            <filter id="glow">
                <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                <feMerge> 
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
        </defs>
        
        <!-- Main circular arc -->
        <path d="M 50 100 A 50 50 0 1 1 150 100" 
              stroke="url(#logoGradient)" 
              stroke-width="8" 
              fill="none" 
              filter="url(#glow)"/>
        
        <!-- Inner arc layers -->
        <path d="M 60 100 A 40 40 0 1 1 140 100" 
              stroke="url(#logoGradient)" 
              stroke-width="4" 
              fill="none" 
              opacity="0.7"/>
        
        <path d="M 70 100 A 30 30 0 1 1 130 100" 
              stroke="url(#logoGradient)" 
              stroke-width="2" 
              fill="none" 
              opacity="0.5"/>
        
        <!-- Circuit lines -->
        <g stroke="url(#logoGradient)" stroke-width="3" fill="none" filter="url(#glow)">
            <!-- Top line -->
            <path d="M 120 80 L 160 80 L 170 80" stroke-linecap="round"/>
            <circle cx="175" cy="80" r="4" fill="url(#logoGradient)"/>
            
            <!-- Middle line -->
            <path d="M 125 100 L 165 100 L 175 100" stroke-linecap="round"/>
            <circle cx="180" cy="100" r="4" fill="url(#logoGradient)"/>
            
            <!-- Bottom line -->
            <path d="M 120 120 L 160 120 L 170 120" stroke-linecap="round"/>
            <circle cx="175" cy="120" r="4" fill="url(#logoGradient)"/>
        </g>
    </svg>
    """

def inject_modern_css():
    """Inject modern, professional CSS styling with enhanced logo integration"""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Root variables for consistent theming */
        :root {
            --primary-bg: #0a0a15;
            --secondary-bg: #151528;
            --accent-bg: #1a1a35;
            --primary-text: #ffffff;
            --secondary-text: #a0aec0;
            --accent-color: #00d4ff;
            --accent-secondary: #667eea;
            --success-color: #48bb78;
            --warning-color: #ed8936;
            --error-color: #f56565;
            --border-color: #2d3748;
            --hover-bg: #2d3748;
            --glow-color: rgba(0, 212, 255, 0.3);
        }
        
        /* Global app styling */
        .stApp {
            background: radial-gradient(ellipse at center, var(--secondary-bg) 0%, var(--primary-bg) 100%);
            color: var(--primary-text);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom header */
        .app-header {
            background: linear-gradient(135deg, var(--accent-color), var(--accent-secondary));
            padding: 1.5rem 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 8px 32px var(--glow-color);
            position: relative;
            overflow: hidden;
        }
        
        .app-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .app-title {
            font-size: 2.8rem;
            font-weight: 700;
            margin: 0;
            background: linear-gradient(45deg, #ffffff, #e2e8f0, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            position: relative;
            z-index: 1;
        }
        
        .app-subtitle {
            font-size: 1.2rem;
            margin: 0.5rem 0 0 0;
            color: rgba(255, 255, 255, 0.9);
            font-weight: 400;
            position: relative;
            z-index: 1;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, var(--secondary-bg) 0%, var(--accent-bg) 100%);
            border-right: 2px solid var(--border-color);
        }
        
        /* Logo container in sidebar */
        .sidebar-logo {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2rem 1rem 1.5rem 1rem;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.05), rgba(102, 126, 234, 0.05));
            border-radius: 16px;
            border: 1px solid rgba(0, 212, 255, 0.2);
            backdrop-filter: blur(20px);
            position: relative;
        }
        
        .sidebar-logo::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, transparent, rgba(0, 212, 255, 0.1), transparent);
            border-radius: 16px;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .sidebar-logo:hover::before {
            opacity: 1;
        }
        
        .logo-svg {
            transition: transform 0.3s ease, filter 0.3s ease;
            filter: drop-shadow(0 4px 12px var(--glow-color));
        }
        
        .logo-svg:hover {
            transform: scale(1.05) rotate(2deg);
            filter: drop-shadow(0 6px 20px var(--glow-color));
        }
        
        .logo-text {
            font-size: 1.8rem;
            font-weight: 700;
            margin-top: 1rem;
            background: linear-gradient(45deg, var(--accent-color), var(--accent-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            letter-spacing: -0.5px;
        }
        
        .logo-tagline {
            font-size: 0.85rem;
            color: var(--secondary-text);
            margin-top: 0.25rem;
            text-align: center;
            font-weight: 400;
        }
        
        .sidebar-section {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid var(--border-color);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .sidebar-section:hover {
            background: rgba(255, 255, 255, 0.05);
            border-color: var(--accent-color);
            box-shadow: 0 4px 20px rgba(0, 212, 255, 0.1);
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
            border-radius: 20px !important;
            padding: 1.5rem !important;
            margin-bottom: 1rem !important;
            max-width: 85% !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* User message */
        .stChatMessage[data-testid="stChatMessage"][data-role="user"] > div {
            background: linear-gradient(135deg, var(--accent-color), var(--accent-secondary)) !important;
            color: white !important;
            margin-left: auto !important;
            box-shadow: 0 8px 32px var(--glow-color);
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
            border: 1px solid var(--accent-color) !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            overflow-x: auto !important;
            font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            position: relative;
        }
        
        pre::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--accent-color), var(--accent-secondary));
        }
        
        code {
            background: rgba(0, 212, 255, 0.15) !important;
            color: var(--accent-color) !important;
            padding: 0.3rem 0.5rem !important;
            border-radius: 6px !important;
            font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
            border: 1px solid rgba(0, 212, 255, 0.3);
        }
        
        /* Input styling */
        .stChatInput > div {
            background: linear-gradient(135deg, var(--secondary-bg), var(--accent-bg)) !important;
            border-radius: 28px !important;
            border: 2px solid var(--border-color) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        .stChatInput > div:focus-within {
            border-color: var(--accent-color) !important;
            box-shadow: 0 8px 32px var(--glow-color) !important;
        }
        
        .stChatInput input {
            background: transparent !important;
            color: var(--primary-text) !important;
            border: none !important;
            font-size: 1rem !important;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, var(--accent-color), var(--accent-secondary)) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 32px rgba(0, 212, 255, 0.5) !important;
        }
        
        .stButton > button:hover::before {
            left: 100%;
        }
        
        /* Text input styling */
        .stTextInput > div > div > input {
            background: var(--secondary-bg) !important;
            color: var(--primary-text) !important;
            border: 2px solid var(--border-color) !important;
            border-radius: 10px !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: var(--accent-color) !important;
            box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1) !important;
        }
        
        /* Select box styling */
        .stSelectbox > div > div {
            background: var(--secondary-bg) !important;
            color: var(--primary-text) !important;
            border: 2px solid var(--border-color) !important;
            border-radius: 10px !important;
        }
        
        /* Metrics styling */
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.05), rgba(102, 126, 234, 0.05)) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        [data-testid="metric-container"]:hover {
            border-color: var(--accent-color);
            box-shadow: 0 4px 20px rgba(0, 212, 255, 0.1);
        }
        
        /* Success/info/warning/error messages */
        .stSuccess, .stInfo, .stWarning, .stError {
            border-radius: 12px !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
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
            border-color: var(--accent-color);
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
            background: linear-gradient(45deg, var(--accent-color), var(--accent-secondary));
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(45deg, #0099cc, #5a67d8);
        }
        
        /* Animation for loading */
        @keyframes pulse {
            0% { opacity: 0.6; }
            50% { opacity: 1; }
            100% { opacity: 0.6; }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-5px); }
        }
        
        .loading {
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        .floating {
            animation: float 3s ease-in-out infinite;
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
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 32px rgba(0, 212, 255, 0.2);
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
        
        /* Message actions */
        .message-actions {
            display: flex;
            gap: 0.5rem;
            margin-top: 0.5rem;
            opacity: 0.7;
            transition: opacity 0.3s ease;
        }
        
        .message-actions:hover {
            opacity: 1;
        }
        
        .action-button {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 0.25rem 0.5rem;
            font-size: 0.75rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .action-button:hover {
            background: var(--accent-color);
            color: white;
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
            <h1 class="app-title">FluxCode</h1>
            <p class="app-subtitle">AI-Powered Code Assistant with Gemini</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def create_sidebar_logo():
    """Create the sidebar logo section"""
    logo_svg = create_logo_svg()
    st.markdown(
        f"""
        <div class="sidebar-logo floating">
            <div class="logo-svg">
                {logo_svg}
            </div>
            <div class="logo-text">FluxCode</div>
            <div class="logo-tagline">AI Code Assistant</div>
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
    """Create enhanced sidebar with logo and multiple sections"""
    with st.sidebar:
        # Logo Section
        create_sidebar_logo()
        
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
                    file_name=f"fluxcode_conversation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
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
        "Detailed": "Provide comprehensive explanations with multiple examples"
    }
    
    if prefix_parts:
        prefix = "You are an expert AI coding assistant. " + ", ".join(prefix_parts) + "."
        if response_style in style_instructions:
            prefix += " " + style_instructions[response_style] + "."
        return prefix + "\n\n" + prompt
    return prompt

def extract_code_blocks(text: str) -> List[Dict[str, str]]:
    """Extract code blocks from markdown text"""
    pattern = r"```(?P<language>\w+)?\n(?P<code>.*?)\n```"
    matches = re.finditer(pattern, text, re.DOTALL)
    return [match.groupdict() for match in matches]

def display_message(message: Dict[str, str]):
    """Display a message in the chat with proper formatting"""
    with st.chat_message(message["role"]):
        content = message["content"]
        
        # Check for code blocks
        code_blocks = extract_code_blocks(content)
        if code_blocks:
            # Split content by code blocks to handle text and code separately
            parts = re.split(r"```\w*\n.*?\n```", content, flags=re.DOTALL)
            
            for i, part in enumerate(parts):
                if part.strip():
                    st.markdown(part)
                if i < len(code_blocks):
                    code_block = code_blocks[i]
                    language = code_block.get("language", "")
                    st.code(code_block["code"], language=language)
        else:
            st.markdown(content)
        
        # Add message actions
        if message["role"] == "assistant":
            with st.expander("Message Actions"):
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Copy", key=f"copy_{message['id']}"):
                        st.session_state.clipboard = content
                        st.toast("Copied to clipboard!")
                with col2:
                    if st.button("🔁 Regenerate", key=f"regenerate_{message['id']}"):
                        # Implement regeneration logic here
                        pass

def generate_response(prompt: str, api_key: str) -> str:
    """Generate a response from Gemini API"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(st.session_state.current_model)
        
        # Format prompt with selected modes
        formatted_prompt = format_response_with_mode(
            prompt,
            st.session_state.code_gen_mode,
            st.session_state.explain_mode,
            st.session_state.debug_mode,
            st.session_state.response_style
        )
        
        response = model.generate_content(formatted_prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None

def main():
    """Main application function"""
    # Initialize the app
    inject_modern_css()
    create_app_header()
    initialize_session_state()
    
    # Create sidebar and get settings
    api_key, code_gen_mode, explain_mode, debug_mode, response_style = create_sidebar()
    st.session_state.code_gen_mode = code_gen_mode
    st.session_state.explain_mode = explain_mode
    st.session_state.debug_mode = debug_mode
    st.session_state.response_style = response_style
    
    # Display chat messages
    for message in st.session_state.messages:
        display_message(message)
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about coding..."):
        if not api_key:
            st.error("Please enter your Gemini API key in the sidebar")
            return
        
        # Add user message to chat history
        user_message = {
            "role": "user",
            "content": prompt,
            "id": f"user_{len(st.session_state.messages)}",
            "timestamp": datetime.datetime.now().isoformat()
        }
        st.session_state.messages.append(user_message)
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.spinner("Generating response..."):
            response = generate_response(prompt, api_key)
            if response:
                assistant_message = {
                    "role": "assistant",
                    "content": response,
                    "id": f"assistant_{len(st.session_state.messages)}",
                    "timestamp": datetime.datetime.now().isoformat()
                }
                st.session_state.messages.append(assistant_message)
                
                # Display assistant message
                display_message(assistant_message)
                
                # Update stats
                st.session_state.message_count += 1
                st.rerun()

if __name__ == "__main__":
    main()
