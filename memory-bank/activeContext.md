# Active Context: AI Conversation Orchestrator

## 1. Current Focus: Project Initialization & Planning

-   **Date:** 2025-05-27 (Pivoted)
-   **Objective:** Simplify project to a Python CLI script based on user feedback. Update all Memory Bank documents.
-   **Status:** Core Memory Bank files (`projectbrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`) are being updated to reflect the Python CLI approach.

## 2. Recent Changes & Decisions

-   **Project Scope Redefined (Python CLI):**
    -   API keys and initial settings (participating AIs, initial message, target AI) loaded from `config.ini`.
    -   Conversation displayed in console and appended to `conversation_log.txt`.
    -   No GUI.
-   **Communication Language:** Castellano.
-   **Product Goals (Adjusted for CLI):** Focus on core functionality and simplicity.
-   **Architecture (Python CLI):** Procedural script with helper functions/classes for AI connectors and config loading.
-   **Technology Stack (Python CLI):** Python 3, `openai`, `google-generativeai`, `anthropic`, `configparser`, `requests` (optional).

## 3. Next Steps (Planning Phase - Python CLI)

1.  Finish updating all Memory Bank files (`progress.md` next).
2.  Outline the structure of `config.ini`.
3.  Define the main Python script structure (`main.py` or `ai_orchestrator.py`).
4.  Detail the functions for each AI connector.
5.  Specify the format for conversation history and log file entries.
6.  Discuss how much conversation history to pass to AIs in the CLI context.
7.  Request API documentation links from the user if needed for specific parameters or provide guidance on where to find them.
8.  Once the Python CLI plan is agreed upon, request the user to switch to "ACT MODE" to begin implementation.

## 4. Active Decisions & Considerations (Python CLI)

-   **Simplicity is Key:** Prioritize a straightforward, functional script.
-   **Configuration File:** `config.ini` for API keys and run settings.
-   **Error Handling:** Essential for API calls and file operations.
-   **Dependencies:** Keep minimal; use official SDKs where possible.
-   **User Guidance:** Clear instructions on how to set up `config.ini` and run the script will be needed.

## 5. Important Patterns & Preferences (Python CLI)

-   **Modularity:** Separate functions for config loading, each AI connector, and logging.
-   **Readability:** Clear variable names and comments.
-   **Robustness:** Basic error handling for common issues.

## 6. Learnings & Project Insights (Post-Pivot)

-   User prefers a simpler, non-GUI approach for the initial version.
-   Python CLI script aligns better with the goal of quick setup and core functionality focus.
-   Managing API interactions and conversation history remains the core challenge, now within a Python script context.
-   Clear console output and a well-formatted log file are important for usability.

*(This document will be updated regularly as the project progresses.)*
