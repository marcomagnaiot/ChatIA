# Tech Context: AI Conversation Orchestrator (Python CLI Script)

## 1. Core Technology

-   **Language:** Python (version 3.x, e.g., 3.8+)
-   **Execution Environment:** Command-Line Interface (CLI). No graphical user interface.

## 2. Key Python Libraries

-   **OpenAI API (for ChatGPT):**
    -   `openai` (Official Python SDK).
-   **Google Gemini API:**
    -   `google-generativeai` (Official Python SDK).
-   **Anthropic Claude API:**
    -   `anthropic` (Official Python SDK).
-   **HTTP Requests (Fallback/Alternative):**
    -   `requests` (If an SDK is not suitable or for direct calls).
-   **Configuration File Parsing:**
    -   `configparser` (Built-in, for `.ini` files).
    -   `json` (Built-in, if using `.json` for config).
    *(Decision: Start with `configparser` for simplicity, e.g., `config.ini`)*
-   **Date/Time (for logging):**
    -   `datetime` (Built-in).

## 3. AI Model APIs & SDKs

-   **OpenAI API (ChatGPT):**
    -   Requires an API key.
    -   Will use the `openai` Python library.
-   **Google Gemini API:**
    -   Requires an API key.
    -   Will use the `google-generativeai` Python library.
-   **Anthropic Claude API:**
    -   Requires an API key.
    -   Will use the `anthropic` Python library.

    *Note: For each API/SDK, we will need to consult their specific documentation for client initialization, request/response formats, authentication, error handling, and rate limits.*

## 4. API Key and Configuration Storage

-   **Local Configuration File:** A plain text file, e.g., `config.ini`.
    -   This file will store:
        -   API keys for each service (Claude, Gemini, ChatGPT).
        -   List of AIs to participate in the conversation.
        -   The initial message/prompt.
        -   The name of the AI to receive the initial message.
        -   (Optional) Number of conversation turns, log file name.
    -   **Security:** This file will contain sensitive API keys. It **MUST** be added to `.gitignore` if the project is ever version controlled to prevent accidental commits. Users will be responsible for creating and populating this file.

## 5. Development Environment

-   **Python 3.x:** Installed on the user's system.
-   **`pip`:** Python package installer (usually comes with Python).
-   **Virtual Environment (Recommended):**
    -   Use `venv` (built-in) to create an isolated environment for the project's dependencies.
    -   Commands: `python -m venv venv_name`, then `source venv_name/bin/activate` (Linux/macOS) or `venv_name\Scripts\activate` (Windows).
-   **Code Editor:** VS Code (as per current environment).
-   **Version Control (Optional for local script, but good practice):** Git.

## 6. Technical Constraints & Considerations (Python CLI)

-   **Synchronous Execution (Default):** Python scripts are generally synchronous. API calls are I/O-bound and will block execution until a response is received. For a simple CLI script where IAs respond one after another, this is acceptable.
    -   *(Future Enhancement: If parallel calls or non-blocking behavior were ever needed, `asyncio` could be introduced, but this adds complexity and is out of scope for the initial simple version.)*
-   **Error Handling:** Robust error handling for API calls (network issues, invalid keys, API errors, SDK exceptions) is crucial. Use `try-except` blocks.
-   **Rate Limiting:** Each AI service will have rate limits. The script needs to handle these gracefully (e.g., print a message, pause, or exit). SDKs might offer some automatic retry mechanisms, but this needs to be checked.
-   **Conversation History Management:**
    -   The script will maintain a list of message objects/dictionaries representing the conversation history.
    -   Each AI SDK will have its own way of accepting this history (e.g., a list of `{'role': 'user'/'assistant', 'content': '...'}` messages). The AI connector functions will need to format the history appropriately.
    -   Decide how much history to send to keep context vs. token limits.
-   **Input/Output:**
    -   Configuration read from `config.ini`.
    -   Conversation printed to standard output (console).
    -   Conversation appended to a log file (e.g., `conversation_log.txt`).
-   **Dependencies:** The user will need to install Python and the required libraries (`pip install openai google-generativeai anthropic requests`). A `requirements.txt` file will be provided.

*(This document reflects the shift to a Python CLI script approach.)*
