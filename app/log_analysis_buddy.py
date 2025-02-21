# log_analysis_buddy.py - Modular Log Analysis Functionality
import os
import csv
import logging
from llm_provider import get_default_provider

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_log_file(file_path):
    """Read the CSV log file and return its contents as a string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            lines = [" ".join(line) for line in reader]
            return "\n".join(lines)
    except Exception as e:
        logging.error(f"Error reading log file: {e}")
        return ""

def analyze_logs(provider_choice, api_key, log_file_path, additional_context, model_string):
    """
    Perform log analysis by:
      - Reading the log file.
      - Constructing the prompt (combining log contents and additional context).
      - Calling the selected LLM provider to generate a response.
    Returns the LLM response as a string.
    """
    logging.info("Starting log analysis...")
    if not os.path.exists(log_file_path):
        logging.error("Log file not found.")
        return None

    log_contents = read_log_file(log_file_path)
    if not log_contents:
        logging.error("No log contents could be read.")
        return None

    prompt_text = f"Perform a detailed security analysis of these logs:\n{log_contents}\n\nAdditional context: {additional_context}"
    logging.info("Constructed prompt for LLM.")

    # Instantiate the appropriate provider.
    if provider_choice == "OpenAI":
        provider = get_default_provider("openai", api_key=api_key)
    else:
        provider = get_default_provider("ollama")

    try:
        response = provider.send_prompt(model_string, prompt_text)
        logging.info("LLM response received successfully.")
        return response
    except Exception as e:
        logging.error(f"Error during LLM call: {e}")
        return None

if __name__ == '__main__':
    # CLI mode (if needed)
    import inquirer
    provider_answer = inquirer.prompt([
        inquirer.List('provider', message="Select LLM Provider", choices=["Ollama", "OpenAI"])
    ])
    provider_choice = provider_answer['provider']
    api_key = ""
    if provider_choice == "OpenAI":
        print("Enter your OpenAI API Key:")
        api_key = input().strip()
    print("Enter the CSV log file path (relative to current directory):")
    log_file = input().strip()
    log_file_path = os.path.join(os.getcwd(), log_file)
    print("Enter any additional context for the analysis:")
    additional_context = input().strip()
    if provider_choice == "OpenAI":
        model_choices = ["gpt-3.5-turbo", "gpt-4"]
    else:
        model_choices = ["Ollama-gpt-4", "Ollama-gpt-3.5"]
    model_answer = inquirer.prompt([
        inquirer.List('model', message="Select the model for this session", choices=model_choices)
    ])
    model_string = model_answer["model"]
    result = analyze_logs(provider_choice, api_key, log_file_path, additional_context, model_string)
    if result:
        print("\n========== LLM Response ==========")
        print(result)
        print("====================================\n")
    else:
        print("Log analysis failed.")
