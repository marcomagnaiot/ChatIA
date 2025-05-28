# AI Orchestrator

A Python application that orchestrates conversations between multiple AI models (ChatGPT, Gemini, and Claude) in a round-robin fashion. The AIs engage in structured dialogues, building upon each other's responses to explore complex topics and generate rich, multi-perspective conversations.

## 🌟 Features

- **Multi-AI Conversations**: Supports ChatGPT (OpenAI), Gemini (Google), and Claude (Anthropic)
- **Round-Robin Dialogue**: AIs take turns responding to each other in a configurable order
- **Flexible Configuration**: Easily customize conversation parameters, AI participants, and model selection
- **Comprehensive Logging**: Dual logging system with detailed timestamps and clean dialogue-only logs
- **Model Selection**: Choose from the latest AI models with different capabilities and pricing
- **Error Handling**: Robust error handling with graceful degradation
- **Security-First**: Template-based configuration to protect API keys

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- API keys for the AI services you want to use:
  - [OpenAI API Key](https://platform.openai.com/api-keys) (for ChatGPT)
  - [Google AI Studio API Key](https://aistudio.google.com/app/apikey) (for Gemini)
  - [Anthropic API Key](https://console.anthropic.com/) (for Claude)

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd ai-orchestrator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up configuration**
   ```bash
   # Copy the template configuration file
   cp config.template.ini config.ini
   
   # Edit config.ini and replace the placeholder API keys with your real ones
   # Example: CHATGPT_API_KEY = sk-your-actual-api-key-here
   ```

4. **Run the program**
   ```bash
   python ai_orchestrator.py
   ```

## 📁 Project Structure

```
ai-orchestrator/
├── ai_orchestrator.py          # Main application file
├── config.template.ini         # Configuration template (safe for version control)
├── config.ini                  # Your actual configuration (ignored by git)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
└── logs/                       # Generated log files (created automatically)
    ├── conversation_log.txt    # Detailed log with timestamps
    └── conversation_alone.txt  # Clean dialogue-only log
```

## ⚙️ Configuration

The application uses `config.ini` for all settings. Here are the key configuration options:

### API Keys
```ini
[API_KEYS]
CHATGPT_API_KEY = your-openai-api-key-here
GEMINI_API_KEY  = your-google-api-key-here
CLAUDE_API_KEY  = your-anthropic-api-key-here
```

### Conversation Settings
```ini
[CONVERSATION_SETTINGS]
# Which AIs participate and in what order
PARTICIPATING_AIS = ChatGPT,Claude

# The message that starts the conversation
INITIAL_MESSAGE = Hello! Let's discuss artificial intelligence.

# Which AI receives the first message
INITIAL_AI_TARGET = ChatGPT

# Number of back-and-forth exchanges after the initial response
NUMBER_OF_TURNS = 10

# How many previous messages each AI sees for context
HISTORY_LENGTH = 5

# Where to save the conversation log
LOG_FILE = conversation_log.txt

# Optional instructions sent to all AIs
SYSTEM_PROMPT = You are a helpful assistant.
```

### Model Selection
```ini
# Choose specific models for each AI service
CHATGPT_MODEL_NAME = gpt-4.1-mini    # Cost-effective option
GEMINI_MODEL_NAME = gemini-2.0-flash  # Fast and efficient
CLAUDE_MODEL_NAME = claude-sonnet-4   # Balanced performance
```

## 🤖 Supported AI Models

### OpenAI (ChatGPT)
- **gpt-4o** - Latest GPT-4 optimized model (high capability, higher cost)
- **gpt-4.1-mini** - Compact version with good performance (recommended for cost-effectiveness)
- **gpt-4.1** - Enhanced GPT-4 with improvements
- **o3** - Advanced reasoning model (specialized use cases)

### Google (Gemini)
- **gemini-2.5-pro-preview** - Latest Pro model (best quality)
- **gemini-2.0-flash** - Current Flash model (recommended for speed)
- **gemini-1.5-pro-latest** - Stable Pro version
- **gemini-1.5-flash-latest** - Stable Flash version

### Anthropic (Claude)
- **claude-opus-4** - Most capable model (highest quality, higher cost)
- **claude-sonnet-4** - Balanced performance and cost (recommended)
- **claude-haiku-3.5** - Fastest and most economical

## 💡 Usage Examples

### Philosophy Debate
```ini
PARTICIPATING_AIS = ChatGPT,Claude
INITIAL_MESSAGE = We are two philosophers debating the nature of consciousness. One argues for materialism, the other for dualism. Begin the debate.
NUMBER_OF_TURNS = 20
SYSTEM_PROMPT = You are a knowledgeable philosopher. Present rigorous arguments and respond thoughtfully to counterarguments.
```

### Creative Writing
```ini
PARTICIPATING_AIS = ChatGPT,Gemini,Claude
INITIAL_MESSAGE = Let's collaboratively write a science fiction story. Start with a character discovering something unusual.
NUMBER_OF_TURNS = 15
SYSTEM_PROMPT = You are a creative writer. Build upon the previous narrative while adding your own creative elements.
```

### Technical Discussion
```ini
PARTICIPATING_AIS = ChatGPT,Claude
INITIAL_MESSAGE = Discuss the pros and cons of different machine learning architectures for natural language processing.
SYSTEM_PROMPT = You are a technical expert. Provide detailed, accurate information and cite relevant research when possible.
```

## 📊 Cost Management

AI API calls cost money based on token usage. Here are some tips to manage costs:

### Cost-Effective Settings
- Use smaller models: `gpt-4.1-mini`, `gemini-2.0-flash`, `claude-haiku-3.5`
- Reduce `NUMBER_OF_TURNS` for shorter conversations
- Lower `HISTORY_LENGTH` to reduce context size
- Test with 2-3 turns before running long conversations

### Monitoring Usage
- Check your API usage dashboards regularly
- Set up billing alerts in your AI service accounts
- Monitor the generated log files to understand token consumption patterns

## 🔧 Troubleshooting

### Common Issues

**"Could not find configuration file"**
- Ensure you've copied `config.template.ini` to `config.ini`
- Check that the file is in the same directory as `ai_orchestrator.py`

**"API key appears to be placeholder"**
- Edit `config.ini` and replace `YOUR_API_KEY_HERE` with your actual API key
- Ensure there are no extra spaces or quotes around the API key

**"AI not recognized"**
- Check spelling in `PARTICIPATING_AIS` (case-sensitive: ChatGPT, Gemini, Claude)
- Ensure the AI name matches exactly

**API Errors**
- Verify your API keys are valid and have sufficient credits
- Check that the model names are correct and currently available
- Some models may have usage restrictions or require special access

### Debug Mode
To debug issues, start with minimal settings:
```ini
PARTICIPATING_AIS = ChatGPT
NUMBER_OF_TURNS = 2
HISTORY_LENGTH = 2
INITIAL_MESSAGE = Hello, how are you?
```

## 🔒 Security Considerations

- **Never commit `config.ini`** with real API keys to version control
- The `.gitignore` file is configured to prevent accidental commits
- Keep your API keys secure and rotate them periodically
- Monitor your API usage for unexpected activity
- Consider using environment variables for API keys in production deployments

## 📝 Log Files

The application generates two types of logs:

### Detailed Log (`conversation_log.txt`)
Contains timestamps, system messages, and full conversation flow:
```
[2025-05-28 16:30:15] System: Starting conversation. Log file: conversation_log.txt
[2025-05-28 16:30:15] USER: Hello! Let's discuss AI.
[2025-05-28 16:30:18] ChatGPT: Hello! I'd be happy to discuss AI with you...
```

### Clean Dialogue Log (`conversation_alone.txt`)
Contains only the conversation without timestamps:
```
USER: Hello! Let's discuss AI.
ChatGPT: Hello! I'd be happy to discuss AI with you...
Claude: That's a fascinating topic. From my perspective...
```

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- Report bugs or suggest features via GitHub issues
- Improve documentation
- Add support for new AI models or services
- Optimize performance or add new features
- Share interesting conversation examples

## 📄 License

This project is open source. Please check the license file for details.

## 🙏 Acknowledgments

- OpenAI for the GPT models and API
- Google for the Gemini models and API
- Anthropic for the Claude models and API
- The Python community for excellent libraries

## 📞 Support

If you encounter issues:

1. Check this README for common solutions
2. Review the configuration template and examples
3. Check the log files for error messages
4. Ensure your API keys are valid and have sufficient credits
5. Create an issue on GitHub with details about your problem

---

**Happy AI orchestrating!** 🎭🤖
