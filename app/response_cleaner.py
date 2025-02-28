import re
import logging
from llm_provider import get_default_provider

def clean_response(text):
    """Function to clean the response and make it presentable in the UI."""
    cleaned_lines = []
    for line in text.splitlines():
        # Collapse multiple spaces into one per line.
        cleaned_line = " ".join(line.split())
        cleaned_lines.append(cleaned_line)
    cleaned_text = "\n".join(cleaned_lines)
    # Ensure Markdown headers have a single space after the '#' characters.
    cleaned_text = re.sub(r'^(#+)\s*', r'\1 ', cleaned_text, flags=re.MULTILINE)
    return cleaned_text

def refactor_response(provider_choice, api_key, model_string, cleaned_text):
    """Function to refactor the response with AI."""
    if provider_choice == "OpenAI":
        provider = get_default_provider("openai", api_key=api_key)
    else:
        provider = get_default_provider("ollama")
    prompt_text = "Take the response and provide a more readable version, using paragraphs and bullet points."
    logging.info("Cleaning the response for readability...")
    try:
        refactored_clean_response = provider.send_prompt(model_string, prompt_text, cleaned_text)
    except Exception as exception_handle:
        logging.error(f"Error during LLM call: {exception_handle}")
        return None
    return refactored_clean_response
  
    