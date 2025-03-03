#// Copyright 2025 Joshua McKiddy. All Rights Reserved.
#// SPDX-License-Identifier: Apache-2.0

import os
import csv
import json
import logging
from llm_provider import get_default_provider

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_csv_log(file_path):
    """Function to read CSV log files and return their contents as a string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            lines = [" ".join(line) for line in reader]
            return "\n".join(lines)
    except Exception as e:
        logging.error(f"Error reading CSV log file: {e}")
        return ""

def read_json_log(file_path):
    """Function to read JSON log files and return their contents as a string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return json.dumps(data, indent=2)
    except Exception as e:
        logging.error(f"Error reading JSON log file: {e}")
        return ""

def read_plain_log(file_path):
    """Function to read plain text log files and return their contents as a string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logging.error(f"Error reading plain log file: {e}")
        return ""

def parse_log_file(file_path):
    """Function to parse log files based on their extension."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".csv":
        return read_csv_log(file_path)
    elif ext == ".json":
        return read_json_log(file_path)
    else:
        return read_plain_log(file_path)

def analyze_logs(provider_choice, api_key, log_file_path, additional_context, model_string):
    """Function to analyze log files using the specified LLM provider."""
    logging.info("Starting log analysis...")
    if not os.path.exists(log_file_path):
        logging.error("Log file not found.")
        return None

    log_contents = parse_log_file(log_file_path)
    if not log_contents:
        logging.error("No log contents could be read.")
        return None

    logging.info("Parsed log file successfully.")

    prompt_text = (
        "Perform a detailed security analysis of the following logs and provide your response as a well-structured "
        "Markdown report with clear headings, bullet points, and paragraphs. Fix any grammatical errors and remove "
        "unnecessary spacing.\n\n"
        "Logs:\n" + log_contents + "\n\n"
        "Additional context:\n" + additional_context
    )
    logging.info("Constructed prompt for LLM.")

    if provider_choice == "OpenAI":
        provider = get_default_provider("openai", api_key=api_key)
    else:
        provider = get_default_provider("ollama")

    try:
        response = provider.send_prompt(model_string, prompt_text)
        logging.info("LLM response received successfully.")
        return response
    except Exception as exception_handle:
        logging.error(f"Error during LLM call: {exception_handle}")
        return None

if __name__ == '__main__':
    # CLI mode disabled for enhancement of the full application
    pass
