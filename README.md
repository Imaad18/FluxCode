![scrnli_gp83L5qxSp64Bc](https://github.com/user-attachments/assets/210ed1ec-03b7-49d1-97ea-e991b92ec4a3)


# Live Demo in Web App = 
https://fluxcode-4lfrzx75adlgcctzv2fzyr.streamlit.app/

# 🚀 CodeFlux - AI Code Assistant



## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Screenshots](#-screenshots)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

## 🌟 Overview

* CodeFlux is a sophisticated AI-powered code assistant that leverages Google's Gemini AI to help developers with coding tasks, debugging, explanations, and more. Built with a modern, professional interface using Streamlit, it offers an intuitive chat-based experience for all your programming needs.

### ✨ Why CodeFlux?

- **🎨 Modern UI**: Professional dark theme with smooth animations
- **🧠 Smart AI**: Powered by Google's latest Gemini models
- **💾 Persistent Sessions**: Save and manage your conversations
- **🔧 Multiple Modes**: Code generation, debugging, and explanation modes
- **📊 Analytics**: Track your usage with built-in statistics
- **🚀 Fast & Responsive**: Optimized for smooth user experience

## 🚀 Features

### Core Functionality
- **Multi-Model Support**: Choose between Gemini 2.0 Flash, 1.5 Pro, and 1.5 Flash
- **Smart Chat Interface**: Clean, modern chat UI with message reactions
- **Code Highlighting**: Syntax highlighting for all major programming languages
- **Export Capabilities**: Download conversations as JSON files

### AI Modes
- **🔨 Code Generation Mode**: Optimized for generating clean, commented code
- **📚 Explanation Mode**: Detailed explanations of code concepts
- **🐛 Debug Mode**: Specialized debugging assistance
- **⚡ Response Styles**: Choose between Concise, Balanced, or Detailed responses

### Session Management
- **💾 Save Conversations**: Persist your chat sessions with custom titles
- **📊 Usage Statistics**: Track messages, session duration, and more
- **🔄 Auto-Save**: Automatically save important conversations
- **📤 Export/Import**: Backup and share your conversations

### Professional Features
- **🎯 Customizable Interface**: Personalize your coding environment
- **⚙️ Advanced Settings**: Fine-tune AI behavior to your preferences
- **📱 Responsive Design**: Works seamlessly on desktop and mobile
- **🔐 Secure**: API keys are handled securely with environment variables

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/codeflux.git
   cd codeflux
   ```

2. **Create virtual environment**
   ```bash
   python -m venv codeflux_env
   source codeflux_env/bin/activate  # On Windows: codeflux_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser** and navigate to `http://localhost:8501`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Required
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional
STREAMLIT_THEME=dark
DEFAULT_MODEL=gemini-2.0-flash
AUTO_SAVE_ENABLED=true
```

### API Key Setup

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and add it to your `.env` file or enter it in the sidebar

## 💻 Usage

### Basic Usage

1. **Start the Application**
   ```bash
   streamlit run app.py
   ```

2. **Enter API Key**: Add your Gemini API key in the sidebar

3. **Choose Your Mode**:
   - Enable **Code Generation Mode** for programming tasks
   - Use **Debug Mode** for troubleshooting code issues
   - Turn on **Explanation Mode** for learning concepts

4. **Start Chatting**: Type your questions in the chat input

### Advanced Features

#### Conversation Management
- **Save**: Click the "💾 Save" button to save current conversation
- **Load**: Click on any saved conversation to load it
- **Export**: Use "📁 Download JSON" to export conversations
- **New**: Start fresh with the "🆕 New" button

#### Response Customization
- **Model Selection**: Choose between different Gemini models
- **Response Style**: Select Concise, Balanced, or Detailed responses
- **Multiple Modes**: Combine different AI modes for optimal results

## 📸 Screenshots

### Main Interface
```
🚀 CodeFlux - Modern chat interface with dark theme
├── Header: Professional gradient header with app branding
├── Chat Area: Clean message bubbles with syntax highlighting
├── Input: Modern chat input with emoji support
└── Sidebar: Feature-rich sidebar with all controls
```

### Key Features Visual
- **Modern Dark Theme**: Professional appearance with cyan accents
- **Message Actions**: Like, dislike, and copy functionality
- **Statistics Dashboard**: Real-time usage metrics
- **Conversation Manager**: Easy save/load functionality

## 📚 API Reference

### Main Functions

#### `initialize_session_state()`
Initializes all session state variables with default values.

#### `save_conversation()`
Saves the current conversation with timestamp and metadata.

#### `format_response_with_mode(prompt, code_gen_mode, explain_mode, debug_mode, response_style)`
Formats user prompts based on selected AI modes and response styles.

#### `create_sidebar()`
Renders the feature-rich sidebar with all controls and settings.

### Session State Variables

| Variable | Type | Description |
|----------|------|-------------|
| `messages` | List | Chat message history |
| `current_model` | String | Active Gemini model |
| `conversation_title` | String | Current conversation title |
| `saved_conversations` | Dict | Stored conversation data |
| `user_preferences` | Dict | User settings and preferences |

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Run tests** (if available)
5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 Python style guidelines
- Add comments for complex functionality
- Update documentation for new features
- Test your changes thoroughly
- Keep commits focused and descriptive

### Areas for Contribution

- 🐛 Bug fixes and improvements
- ✨ New AI modes and features
- 🎨 UI/UX enhancements
- 📚 Documentation improvements
- 🧪 Test coverage expansion
- 🌐 Internationalization

## 🔧 Troubleshooting

### Common Issues

#### API Key Problems
```
Error: Invalid API key
Solution: Verify your Gemini API key is correct and active
```

#### Installation Issues
```
Error: Package conflicts
Solution: Use a fresh virtual environment
```

#### Performance Issues
```
Issue: Slow response times
Solution: Try switching to a faster Gemini model like gemini-2.0-flash
```

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/codeflux/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/codeflux/discussions)
- **Documentation**: Check this README and inline code comments

## 📋 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 512MB minimum (1GB+ recommended)
- **Storage**: 100MB for installation
- **Network**: Internet connection for AI API calls
- **Browser**: Modern web browser (Chrome, Firefox, Safari, Edge)

## 🔮 Roadmap

### Upcoming Features

- [ ] **Plugin System**: Extensible architecture for custom AI modes
- [ ] **Code Execution**: Run and test code directly in the interface
- [ ] **Collaboration**: Share conversations with team members
- [ ] **Themes**: Multiple UI themes and customization options
- [ ] **Voice Input**: Speech-to-text functionality
- [ ] **Mobile App**: Dedicated mobile application
- [ ] **Integration**: GitHub, VS Code, and other tool integrations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google AI Team** for the powerful Gemini AI models
- **Streamlit Team** for the amazing web framework
- **Open Source Community** for inspiration and contributions
- **Contributors** who help make CodeFlux better

---

<div align="center">

**Made with ❤️ by developers, for developers**

[⭐ Star this repo](https://github.com/yourusername/codeflux) • [🐛 Report Bug](https://github.com/yourusername/codeflux/issues) • [💡 Request Feature](https://github.com/yourusername/codeflux/issues)

</div>
