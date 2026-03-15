<div align="center">

![FluxCode Banner](banner.jpeg)

# FluxCode — AI Code Assistant

**An AI-powered coding companion built on Google Gemini**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Powered%20by-Gemini%20AI-4285F4?logo=google&logoColor=white)](https://aistudio.google.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-FF4B4B?logo=streamlit)](https://fluxcode-4lfrzx75adlgcctzv2fzyr.streamlit.app/)

[**Try Live Demo →**](https://fluxcode-4lfrzx75adlgcctzv2fzyr.streamlit.app/)

</div>

---

## Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## Overview

FluxCode is a sophisticated AI-powered code assistant that leverages Google's Gemini AI to help developers with coding tasks, debugging, explanations, and more. Built with a modern, professional dark-theme interface using Streamlit, it offers an intuitive chat-based experience for all your programming needs.

### Why FluxCode?

| Feature | Description |
|---|---|
| **Modern UI** | Professional dark theme with smooth animations and glassmorphism effects |
| **Smart AI** | Powered by Google's latest Gemini 2.0 Flash and 1.5 Pro models |
| **Persistent Sessions** | Save, load, and export conversations with full metadata |
| **Multiple Modes** | Combine code generation, debugging, and explanation modes |
| **Session Analytics** | Track messages and session duration in real time |
| **Multi-turn Chat** | Full conversation history passed to the model for context-aware responses |

---

## Features

### AI Modes
- **Code Generation Mode** — Generates clean, well-commented code for any task
- **Explanation Mode** — Detailed conceptual breakdowns for learning
- **Debug Mode** — Targeted debugging assistance with issue identification
- **Response Styles** — Choose Concise, Balanced, or Detailed verbosity

### Model Support
| Model | Best For |
|---|---|
| `gemini-2.0-flash` | Fast responses, everyday coding tasks |
| `gemini-1.5-pro` | Complex reasoning, large context windows |
| `gemini-1.5-flash` | Balanced speed and capability |

### Session Management
- Save conversations with custom titles
- Load any previously saved session
- Export conversations as JSON
- Auto-save support

---

## Installation

### Prerequisites
- Python 3.8+
- Google Gemini API key — [get one free at Google AI Studio](https://aistudio.google.com/app/apikey)

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Imaad18/FluxCode.git
cd FluxCode

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your API key
echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env

# 5. Run the app
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## Configuration

Create a `.env` file in the project root:

```env
# Required
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional
DEFAULT_MODEL=gemini-2.0-flash
AUTO_SAVE_ENABLED=true
```

### Getting an API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **Create API key**
4. Paste the key into your `.env` file, or enter it directly in the sidebar

---

## Usage

### Basic Workflow

1. Launch the app with `streamlit run app.py`
2. Enter your Gemini API key in the sidebar
3. Select your AI mode(s) and response style
4. Type your question in the chat input and press Enter

### Conversation Management

| Action | How To |
|---|---|
| Save | Click **💾 Save** in the sidebar |
| Load | Click any saved conversation title |
| Delete | Click **🗑️** next to the conversation |
| Export | Click **📁 Download JSON** |
| New chat | Click **🆕 New** (auto-saves if enabled) |

### Combining Modes

You can enable multiple modes simultaneously for richer responses — e.g., enable both **Code Generation** and **Explanation** to get code with a walkthrough, or combine **Debug** and **Explanation** for annotated bug analysis.

---

## API Reference

### Core Functions

| Function | Description |
|---|---|
| `initialize_session_state()` | Sets up all session variables with defaults |
| `generate_response(prompt, api_key)` | Calls Gemini API with full conversation history |
| `format_response_with_mode(prompt)` | Prepends system instructions based on active modes |
| `save_conversation()` | Persists current chat with timestamp and metadata |
| `load_conversation(conv_id)` | Restores a saved conversation by ID |
| `export_conversation()` | Serializes current chat to a JSON string |
| `create_sidebar()` | Renders the full sidebar UI and returns the API key |
| `display_message(message)` | Renders a chat message with syntax-highlighted code blocks |

### Session State Variables

| Variable | Type | Description |
|---|---|---|
| `messages` | `List[Dict]` | Full chat history with role, content, id, timestamp |
| `current_model` | `str` | Active Gemini model identifier |
| `conversation_title` | `str` | Title of the current session |
| `saved_conversations` | `Dict` | All persisted conversations keyed by ID |
| `user_preferences` | `Dict` | Theme, response style, and auto-save settings |
| `code_gen_mode` | `bool` | Code Generation mode toggle |
| `explain_mode` | `bool` | Explanation mode toggle |
| `debug_mode` | `bool` | Debug mode toggle |
| `response_style` | `str` | `"Concise"` / `"Balanced"` / `"Detailed"` |

---

## Contributing

Contributions are welcome! To get started:

```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
# ... make changes ...
git commit -m "feat: add your feature"
git push origin feature/your-feature-name
# Open a pull request
```

### Guidelines
- Follow [PEP 8](https://pep8.org/) style
- Write clear, descriptive commit messages
- Update this README if you add or change features
- Test your changes before submitting

### Areas for Contribution
- New AI modes or prompt templates
- UI/UX improvements
- Test coverage
- Internationalization (i18n)
- Plugin/extension architecture

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `Invalid API key` | Verify the key at [Google AI Studio](https://aistudio.google.com/app/apikey) and ensure it's active |
| Package conflicts | Use a fresh virtual environment |
| Slow responses | Switch to `gemini-2.0-flash` in the sidebar |
| App crashes on start | Ensure Python 3.8+ and all dependencies are installed |

For other issues, open a [GitHub Issue](https://github.com/Imaad18/FluxCode/issues).

---

## System Requirements

- **Python:** 3.8+
- **RAM:** 512 MB minimum (1 GB+ recommended)
- **Storage:** ~100 MB
- **Network:** Required (Gemini API calls)
- **Browser:** Any modern browser (Chrome, Firefox, Safari, Edge)

---

## Roadmap

- [ ] Code execution sandbox — run and test code directly in the UI
- [ ] Team collaboration — share conversations with others
- [ ] Additional themes and customization options
- [ ] Voice input via speech-to-text
- [ ] VS Code extension integration
- [ ] Plugin system for custom AI modes

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

- [Google AI](https://ai.google.dev/) for the Gemini models
- [Streamlit](https://streamlit.io/) for the web framework
- All contributors who help improve FluxCode

---

<div align="center">

Made with ❤️ for developers

[⭐ Star this repo](https://github.com/Imaad18/FluxCode) · [🐛 Report a bug](https://github.com/Imaad18/FluxCode/issues) · [💡 Request a feature](https://github.com/Imaad18/FluxCode/issues)

</div>
