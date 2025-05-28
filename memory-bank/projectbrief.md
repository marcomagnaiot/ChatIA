# Project Brief: AI Conversation Orchestrator

## 1. Project Overview

The project aims to create an application that allows users to input API keys for various Large Language Models (LLMs) such as Claude, Gemini, and ChatGPT. The application will then facilitate a "conversation" between these AI models, where one AI's output becomes the input for the next, creating a chain of dialogue.

## 2. Core Requirements

-   **API Key Management:** Load API keys from a local configuration file (e.g., `config.ini` or `apikeys.json`).
-   **AI Model Integration:** Connect to the respective AI model APIs using Python libraries.
-   **Conversation Flow Control:**
    -   Allow users to define participating AIs, initial message, and first AI recipient, potentially via the configuration file or command-line inputs.
    -   Interaction method: round-robin.
-   **Conversation Display:** Print the ongoing conversation to the command-line console.
-   **Conversation Storage:** Append the full conversation to a local text file (e.g., `conversation_log.txt`).
-   **User Interface:** Command-Line Interface (CLI) only. No graphical user interface.

## 3. Goals

-   To create a platform for observing and experimenting with multi-AI interactions.
-   To enable users to generate unique content or insights by leveraging the combined capabilities of different AI models.
-   To provide a tool for exploring the nuances and differences in responses from various AIs.

## 4. Scope

-   **In Scope (Initial Version - Simplified Python Script):**
    -   Support for Claude, Gemini, and ChatGPT.
    -   Basic conversation flow (user-defined first AI, then sequential turn-taking).
    -   API keys and initial settings loaded from a local configuration file.
    -   Command-line script written in Python.
    -   Conversation displayed in console and appended to a local log file.
-   **Out of Scope (Initial Version):**
    -   Advanced conversation strategies (e.g., AI-driven moderation, dynamic participant selection).
    -   Cloud-based API key storage or user accounts.
    -   Real-time collaboration features.
    -   Commercial deployment or scaling.

## 5. Key Assumptions

-   Users will provide their own valid API keys for the AI services.
-   The primary interaction will be text-based.
-   The application will run as a Python script on the user's local machine.
