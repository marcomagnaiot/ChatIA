import configparser
import datetime
import openai
import google.generativeai as genai
from anthropic import Anthropic
# import requests # Uncomment if needed

# Constants for AI names (to avoid typos)
CHATGPT = "ChatGPT"
GEMINI = "Gemini"
CLAUDE = "Claude"

def load_config(config_file="config.ini"):
    """Loads configuration from the config.ini file."""
    config = configparser.ConfigParser()
    # Specify encoding='utf-8' to avoid UnicodeDecodeError on Windows
    if not config.read(config_file, encoding='utf-8'):
        print(f"Error: Could not find or read the configuration file '{config_file}'.")
        print("Please ensure the file exists and has the correct format and UTF-8 encoding.")
        print("\nIf this is your first time running the program:")
        print("1. Copy 'config.template.ini' to 'config.ini'")
        print("2. Edit 'config.ini' and replace the placeholder API keys with your real ones")
        print("3. You can get API keys from:")
        print("   - OpenAI: https://platform.openai.com/api-keys")
        print("   - Google AI Studio: https://aistudio.google.com/app/apikey")
        print("   - Anthropic: https://console.anthropic.com/")
        return None
    
    # Check if API keys are still placeholders
    try:
        api_keys_section = config['API_KEYS']
        placeholder_keys = []
        
        for key_name, key_value in api_keys_section.items():
            if not key_value or 'YOUR_' in key_value.upper() or 'PLACEHOLDER' in key_value.upper():
                placeholder_keys.append(key_name)
        
        if placeholder_keys:
            print("Warning: The following API keys appear to be placeholders:")
            for key in placeholder_keys:
                print(f"  - {key}")
            print("\nPlease edit 'config.ini' and replace these with your actual API keys.")
            print("The program will continue but may fail when trying to use AIs with placeholder keys.")
    except KeyError:
        print("Warning: No [API_KEYS] section found in config.ini")
    
    return config

def log_message(speaker, message, log_file_path):
    """Logs a message to the console and log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {speaker}: {message}"
    print(formatted_message)
    try:
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(formatted_message + "\n")
    except IOError as e:
        print(f"Error writing to log file '{log_file_path}': {e}")

def log_chat_only(speaker, message, chat_log_filepath):
    """Logs only the dialogue to a separate file (without timestamps)."""
    formatted_message = f"{speaker}: {message}"
    try:
        with open(chat_log_filepath, "a", encoding="utf-8") as f:
            f.write(formatted_message + "\n")
    except IOError as e:
        print(f"Error writing to chat-only log file '{chat_log_filepath}': {e}")

# --- Connector Functions for each AI ---
def get_chatgpt_response(api_key, model_name, prompt, history, system_prompt):
    """Gets a response from ChatGPT using OpenAI API."""
    try:
        client = openai.OpenAI(api_key=api_key)
        
        # Format the conversation history for OpenAI API
        # OpenAI expects: [{"role": "system/user/assistant", "content": "..."}]
        formatted_api_history = []
        
        # Add system prompt if provided
        if system_prompt:
            formatted_api_history.append({"role": "system", "content": system_prompt})

        # Convert our history format to OpenAI format
        # Our format: {'role': 'user'/'assistant', 'name': 'AI_NAME' (optional), 'content': '...'}
        # OpenAI format: {'role': 'user'/'assistant', 'content': '...'}
        for h_msg in history:
            # If the message has 'name', it's an AI response ('assistant')
            # If it doesn't have 'name' and role is 'user', it's a user message
            api_role = "assistant" if h_msg.get("name") else "user"
            
            # Only include valid 'user' and 'assistant' roles for OpenAI API
            if api_role in ["user", "assistant"]:
                formatted_api_history.append({"role": api_role, "content": h_msg["content"]})
            else:
                # This shouldn't happen if our conversation_history is well-formed
                print(f"Warning: Message with non-standard role '{h_msg.get('role')}' omitted for ChatGPT: {h_msg.get('content')[:50]}...")

        # Add the current prompt as a 'user' message
        # In our conversation flow, the 'prompt' is what the current AI should respond to
        formatted_api_history.append({"role": "user", "content": prompt})

        # Make the API call
        response = client.chat.completions.create(
            model=model_name,
            messages=formatted_api_history
        )
        
        # Check if there are choices and message content
        if response.choices and response.choices[0].message:
            return response.choices[0].message.content
        else:
            print("Error: OpenAI API response did not have the expected format.")
            return "Error in ChatGPT response."
            
    except openai.APIError as e:
        print(f"OpenAI API error (ChatGPT): {e}")
        raise Exception(f"ChatGPT API error: {e}")
    except Exception as e:
        print(f"Unexpected error in get_chatgpt_response: {e}")
        raise Exception(f"Unexpected error in ChatGPT: {e}")

def get_gemini_response(api_key, model_name_config, prompt, history, system_prompt):
    """Gets a response from Gemini using Google Generative AI API."""
    try:
        genai.configure(api_key=api_key)
        
        # Model configuration
        generation_config = {
            "temperature": 0.7,  # Adjustable creativity level
            # "top_p": 1,
            # "top_k": 1,
            # "max_output_tokens": 2048,
        }

        # Safety settings - adjust as needed for your use case
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        # Create the model with system instruction if provided
        model = genai.GenerativeModel(
            model_name=model_name_config,
            safety_settings=safety_settings,
            generation_config=generation_config,
            system_instruction=system_prompt if system_prompt else None
        )

        # Convert our history format to Gemini format
        # Our format: {'role': 'user'/'assistant', 'name': 'AI_NAME' (optional), 'content': '...'}
        # Gemini format: {'role': 'user'/'model', 'parts': ["text"]}
        gemini_history = []
        for msg in history:
            # 'assistant' maps to 'model' in Gemini API
            role = "model" if msg.get("name") else "user"
            if role in ["user", "model"]:
                gemini_history.append({'role': role, 'parts': [msg["content"]]})
            else:
                print(f"Warning: Non-standard role '{msg.get('role')}' omitted for Gemini: {msg.get('content')[:50]}...")
        
        # Start a chat with the formatted history
        chat = model.start_chat(history=gemini_history if gemini_history else None)
        
        # Send the current prompt
        response = chat.send_message(prompt)
        
        if response and response.text:
            return response.text
        else:
            # Sometimes Gemini blocks responses due to safety filters
            block_reason = response.prompt_feedback if hasattr(response, 'prompt_feedback') else "Unknown reason"
            print(f"Error: Gemini response was blocked or had no content. Reason: {block_reason}")
            return f"Error in Gemini response (possibly blocked due to safety filters: {block_reason})."

    except Exception as e:
        print(f"Google Gemini API error: {e}")
        raise Exception(f"Gemini API error: {e}")

def get_claude_response(api_key, model_name_config, prompt, history, system_prompt):
    """Gets a response from Claude using Anthropic API."""
    try:
        client = Anthropic(api_key=api_key)
        
        # Format the history for Claude API (Messages API)
        # Claude expects: [{'role': 'user'/'assistant', 'content': '...'}]
        # Our format is already compatible, we just need to map 'name' to 'assistant'
        claude_messages = []
        for msg in history:
            role = "assistant" if msg.get("name") else "user"
            if role in ["user", "assistant"]:
                claude_messages.append({"role": role, "content": msg["content"]})
            else:
                print(f"Warning: Non-standard role '{msg.get('role')}' omitted for Claude: {msg.get('content')[:50]}...")

        # Add the current prompt as a 'user' message
        claude_messages.append({"role": "user", "content": prompt})

        # Make the API call
        response = client.messages.create(
            model=model_name_config,
            max_tokens=2048,  # Adjustable - could be made configurable
            system=system_prompt if system_prompt else None,
            messages=claude_messages
        )

        # Parse the response
        if response.content and isinstance(response.content, list) and len(response.content) > 0:
            # Claude's response is a list of content blocks
            # Usually, for text, the first block is of type 'text'
            block = response.content[0]
            if block.type == "text":
                return block.text
            else:
                print(f"Error: Claude's first content block is not text (type: {block.type}).")
                return "Error in Claude response format."
        else:
            print("Error: Claude response did not have the expected format (no content or empty list).")
            return "Error in Claude response."

    except Exception as e:
        print(f"Anthropic Claude API error: {e}")
        raise Exception(f"Claude API error: {e}")

def main_conversation_loop():
    """Main function that orchestrates the AI conversation."""
    config = load_config()
    if not config:
        return

    try:
        # Load API keys
        chatgpt_api_key = config.get("API_KEYS", "CHATGPT_API_KEY", fallback=None)
        gemini_api_key = config.get("API_KEYS", "GEMINI_API_KEY", fallback=None)
        claude_api_key = config.get("API_KEYS", "CLAUDE_API_KEY", fallback=None)

        # Load conversation settings
        participating_ais_str = config.get("CONVERSATION_SETTINGS", "PARTICIPATING_AIS", fallback="ChatGPT")
        initial_message = config.get("CONVERSATION_SETTINGS", "INITIAL_MESSAGE", fallback="Hello.")
        initial_ai_target_name = config.get("CONVERSATION_SETTINGS", "INITIAL_AI_TARGET", fallback=None)
        num_turns = config.getint("CONVERSATION_SETTINGS", "NUMBER_OF_TURNS", fallback=5)
        history_length = config.getint("CONVERSATION_SETTINGS", "HISTORY_LENGTH", fallback=4)
        log_file = config.get("CONVERSATION_SETTINGS", "LOG_FILE", fallback="conversation_log.txt")
        chat_only_log_file = "conversation_alone.txt"  # Separate log file for just the dialogue
        system_prompt = config.get("CONVERSATION_SETTINGS", "SYSTEM_PROMPT", fallback="").strip()
        if not system_prompt: 
            system_prompt = None
        
        # Load model names
        chatgpt_model_name = config.get("CONVERSATION_SETTINGS", "CHATGPT_MODEL_NAME", fallback="gpt-3.5-turbo")
        gemini_model_name = config.get("CONVERSATION_SETTINGS", "GEMINI_MODEL_NAME", fallback="gemini-1.5-flash-latest")
        claude_model_name = config.get("CONVERSATION_SETTINGS", "CLAUDE_MODEL_NAME", fallback="claude-3-haiku-20240307")

    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"Error in configuration file: {e}")
        return
    except ValueError as e:
        print(f"Error in configuration value (e.g. NUMBER_OF_TURNS must be a number): {e}")
        return

    # Parse participating AIs
    participating_ais = [ai.strip() for ai in participating_ais_str.split(',')]
    if not participating_ais:
        print("Error: No participating AIs specified in configuration.")
        return

    # Mapping of AI names to their connector functions, API keys, and model names
    ai_functions_map = {
        CHATGPT: (get_chatgpt_response, chatgpt_api_key, chatgpt_model_name),
        GEMINI: (get_gemini_response, gemini_api_key, gemini_model_name),
        CLAUDE: (get_claude_response, claude_api_key, claude_model_name),
    }

    # Validate that participating AIs have valid API keys
    active_ais_with_keys = []
    for ai_name in participating_ais:
        if ai_name not in ai_functions_map:
            print(f"Warning: AI '{ai_name}' not recognized. Will be ignored.")
            continue
        _, api_key, _ = ai_functions_map[ai_name]
        if not api_key or "YOUR_" in api_key.upper() or "PLACEHOLDER" in api_key.upper():
            print(f"Warning: API key for '{ai_name}' not configured or is a placeholder. '{ai_name}' will be ignored.")
            continue
        active_ais_with_keys.append(ai_name)
    
    if not active_ais_with_keys:
        print("Error: None of the participating AIs have a valid API key configured.")
        print("Please check your config.ini file and ensure you have replaced the placeholder API keys with real ones.")
        return
    
    participating_ais = active_ais_with_keys  # Update to only active AIs with valid keys

    # Determine the initial target AI
    if initial_ai_target_name and initial_ai_target_name in participating_ais:
        initial_ai_target = initial_ai_target_name
    else:
        initial_ai_target = participating_ais[0]
        if initial_ai_target_name:  # If specified but not valid
            log_message("System", f"Warning: INITIAL_AI_TARGET '{initial_ai_target_name}' is not valid or doesn't have API key. Using '{initial_ai_target}' as first AI.", log_file)

    # Initialize conversation history
    conversation_history = []  # List of dictionaries: {'role': 'user'/'assistant', 'name': 'AI_NAME' (optional), 'content': '...'}

    # Log conversation start
    log_message("System", f"Starting conversation. Log file: {log_file}", log_file)
    log_message("System", f"Participating AIs: {', '.join(participating_ais)}", log_file)
    log_message("System", f"Initial message for {initial_ai_target}: '{initial_message}'", log_file)

    # Send initial message to the first AI
    current_prompt = initial_message
    current_ai_name = initial_ai_target
    ai_function, api_key, model_name_for_call = ai_functions_map[current_ai_name]

    log_message("USER", current_prompt, log_file)
    log_chat_only("USER", current_prompt, chat_only_log_file)
    conversation_history.append({"role": "user", "content": current_prompt})
    
    try:
        # For the first message, there's no conversation history yet
        history_slice_for_first_call = []
        response_text = ai_function(api_key, model_name_for_call, current_prompt, history_slice_for_first_call, system_prompt)
    except Exception as e:
        log_message("System", f"Error calling {current_ai_name}: {e}", log_file)
        return

    log_message(current_ai_name, response_text, log_file)
    log_chat_only(current_ai_name, response_text, chat_only_log_file)
    conversation_history.append({"role": "assistant", "name": current_ai_name, "content": response_text})

    # Main conversation loop - continue with remaining AIs
    try:
        current_ai_index = participating_ais.index(current_ai_name)
    except ValueError:
        log_message("System", f"Error: Initial AI '{current_ai_name}' is not in the list of active AIs. Terminating.", log_file)
        return

    for turn in range(num_turns):
        log_message("System", f"--- Turn {turn + 1} of {num_turns} ---", log_file)
        
        # Move to the next AI in the rotation
        current_ai_index = (current_ai_index + 1) % len(participating_ais)
        current_ai_name = participating_ais[current_ai_index]
        ai_function, api_key, model_name_for_call = ai_functions_map[current_ai_name]

        # The prompt for the current AI is the last response from the previous AI
        if not conversation_history or conversation_history[-1]["role"] != "assistant":
            log_message("System", "Error: Expected an AI response as the last message in history.", log_file)
            break 
        current_prompt = conversation_history[-1]["content"]

        # Prepare conversation history for the current AI
        # Take the last `history_length` messages for context
        history_for_ai = conversation_history[-history_length:]

        log_message("System", f"Sending to {current_ai_name} (model: {model_name_for_call}): '{current_prompt[:100]}...'", log_file)
        
        try:
            response_text = ai_function(api_key, model_name_for_call, current_prompt, history_for_ai, system_prompt)
        except Exception as e:
            log_message("System", f"Error calling {current_ai_name}: {e}", log_file)
            break  # Exit the loop if an AI fails

        log_message(current_ai_name, response_text, log_file)
        log_chat_only(current_ai_name, response_text, chat_only_log_file)
        conversation_history.append({"role": "assistant", "name": current_ai_name, "content": response_text})

    log_message("System", "Conversation finished.", log_file)

if __name__ == "__main__":
    main_conversation_loop()
