# System Patterns: AI Conversation Orchestrator

## 1. Core Architecture (Python CLI Script)

The Python script will consist of the following main logical components:

-   **Configuration Loader:** Reads API keys, participating AIs, initial message, and target AI from a configuration file (e.g., `config.ini` or `config.json`).
-   **AI Service Connectors (Adapters/Clients):** Python functions or classes for each supported AI (Claude, Gemini, ChatGPT). Each connector will:
    -   Take a prompt (string) and conversation history (list of messages).
    -   Use the appropriate Python SDK (e.g., `openai`, `google-generativeai`, `anthropic`) or direct HTTP requests (`requests` library) to call the AI service.
    -   Handle authentication with the API key.
    -   Parse the response.
    -   Return the AI's message as a string.
-   **Conversation Engine (Orchestrator Logic):**
    -   Initializes the conversation with the user-defined first message to the target AI.
    -   Manages the sequence of AI turns (round-robin).
    -   Passes the conversation history (and the last message) to the next AI.
    -   Collects responses.
-   **Output Handler:**
    -   Prints each turn of the conversation (who said what) to the console.
    -   Appends each turn to a local log file (`conversation_log.txt`).

## 2. Key Design Patterns (Potential)

-   **Modular Functions/Classes:** For AI Service Connectors. While a formal Adapter Pattern with interfaces might be overkill for a simple script, the idea of separate, well-defined functions/classes for each AI service remains.
    -   Example function signature: `get_chatgpt_response(api_key: str, prompt: str, history: list) -> str`.
-   **Procedural Flow:** The main script will likely follow a procedural flow for managing the conversation loop.

## 3. Data Flow (Python CLI Script)

1.  Script starts.
2.  **Configuration Loader** reads `config.ini` (or similar) for API keys, list of AIs to use, initial message, and target for the initial message.
3.  **Conversation Engine** initializes an empty conversation history list.
4.  The initial message is sent to the specified target AI using its **AI Service Connector**.
    a.  Connector function is called with API key, initial message, and empty history.
    b.  Connector calls the AI's API.
    c.  AI responds. Connector returns the response string.
5.  **Output Handler** prints "User: [initial message]" and "TargetAI: [response]" to console and appends to `conversation_log.txt`.
6.  The response is added to the conversation history.
7.  **Conversation Engine** enters a loop for subsequent turns, cycling through the selected AIs (round-robin):
    a.  Takes the last AI's response as the new prompt for the current AI in the cycle.
    b.  Calls the current AI's **Service Connector** with its API key, the new prompt, and the conversation history.
    c.  Connector calls the AI's API.
    d.  AI responds. Connector returns the response string.
    e.  **Output Handler** prints "CurrentAI: [response]" to console and appends to `conversation_log.txt`.
    f.  The response is added to the conversation history.
    g.  Loop continues for a set number of turns or until a stop condition (e.g., user interrupt, specific keyword).

## 4. API Key Handling (Python CLI Script)

-   Keys will be stored by the user in a local configuration file (e.g., `config.ini` or `apikeys.json`). This file should be added to `.gitignore` if the project is version controlled.
-   The script's **Configuration Loader** will read these keys at startup.
-   Keys are held in memory during the script's execution and passed to the respective AI Service Connectors.

## 5. Modularity and Extensibility

-   The design should aim to make adding support for new AI models as straightforward as possible, primarily by creating a new `Adapter` implementation.
-   The core Conversation Engine logic should be decoupled from the specifics of any particular AI API.

*(This document will be updated as design decisions are finalized and the system is built.)*
