# Project Progress: AI Conversation Orchestrator

## 1. Overall Status

-   **Current Phase:** Pivoted to Python CLI. Planning Finalized - Ready for Initial Development (ACT MODE).
-   **Last Updated:** 2025-05-27
-   **Next Milestone:** Create main Python script structure (`ai_orchestrator.py`) and `config.ini` template.

## 2. What Works (Conceptual)

-   The core idea of an AI conversation orchestrator is defined.
-   Initial documentation structure (Memory Bank) is in place.
-   Technology choices confirmed: Python CLI, `config.ini` for API keys and settings, console output, and local log file (`conversation_log.txt`).
-   Key architectural patterns (Adapter for AI services) have been identified.

## 3. What's Left to Build (High-Level - Python CLI)

-   **Main Python Script (`ai_orchestrator.py`):**
    -   Overall script structure (e.g., main function, helper functions).
    -   Main loop for conversation turns.
-   **Configuration Management (e.g., in `config_handler.py` or within main script):**
    -   Function to read `config.ini` using `configparser`.
    -   Error handling for missing config file or essential keys/sections.
-   **AI Service Connectors (e.g., in `ai_clients.py` or as separate functions):**
    -   `call_chatgpt(api_key: str, prompt: str, history: list) -> str`
    -   `call_gemini(api_key: str, prompt: str, history: list) -> str`
    -   `call_claude(api_key: str, prompt: str, history: list) -> str`
    -   Each function will use the respective Python SDK (`openai`, `google-generativeai`, `anthropic`) to interact with the APIs, handle authentication, and parse responses.
-   **Conversation Engine (Logic within `ai_orchestrator.py`):**
    -   Initialize conversation history list.
    -   Manage turn-taking: use the initial message for the specified first AI, then round-robin for subsequent turns among selected AIs.
    -   Format and pass conversation history appropriately to each AI connector.
-   **Output and Logging (Logic within `ai_orchestrator.py` or a `logger.py`):**
    -   Print conversation turns to the console (e.g., `USER: ...`, `CHATGPT: ...`).
    -   Append conversation turns to `conversation_log.txt`, including timestamps.

## 4. Known Issues & Blockers (Potential - Python CLI)

-   **API Key Security:** API keys stored in `config.ini` are in plain text. The user is responsible for securing this file (e.g., file permissions, not committing to public Git repos).
-   **Rate Limiting:** Each AI service has rate limits. The script should implement basic error handling for rate limit exceptions (e.g., print a message, exit gracefully).
-   **Varying API/SDK Behaviors:** Each AI SDK might have different ways of handling conversation history, system prompts, and error responses. Connectors must adapt to these.
-   **Context Window Management:** Deciding how much history to send to each AI to maintain context without exceeding token limits or incurring high costs remains an important consideration. This might be a configurable parameter.
-   **Dependency Management:** User will need to install Python and required libraries (e.g., via `pip install -r requirements.txt`).

## 5. Evolution of Project Decisions

-   **[2025-05-27]:** Initial decision for Web App (React/Vite). User feedback incorporated. **Pivoted to Python CLI script** for simplicity. All Memory Bank documents updated to reflect this new direction.

*(This document will track the project's journey, including completed features, ongoing tasks, and any pivots in design or technology.)*
