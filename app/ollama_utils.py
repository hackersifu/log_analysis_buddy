#// Copyright 2025 Joshua McKiddy. All Rights Reserved.
#// SPDX-License-Identifier: Apache-2.0

import subprocess
import threading
import logging
import ollama
import langchain
import socket

ollama.api_url = "http://localhost:11434/api"

def list_local_models():
    """Function to list local Ollama models."""
    try:
        local_models = ollama.list()  # Expected to be a dict, e.g., {"models": [ {...}, {...} ]}
        models_data = local_models.get("models", [])
        model_list = []
        for model_info in models_data:
            model_list.append(model_info.get("model"))
        return model_list
    except Exception as exception_handle:
        logging.error(exception_handle)
        return f"Error: {exception_handle}"

def pull_model(model_name):
    """Function to pull an Ollama model."""
    try:
        model = ollama.pull(model_name)
        return model
    except Exception as e:
        logging.error(e)
        return f"Error pulling model {model_name}: {e}"

def is_port_in_use(port, host="127.0.0.1"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def start_ollama_service():
    """Function to start the Ollama service in a background thread."""
    # Check if port 11434 is already in use.
    if is_port_in_use(11434):
        return "Ollama service is already running."

    def run_service():
        try:
            # This command starts the service; it will run indefinitely.
            subprocess.run(["ollama", "serve"], check=True)
        except Exception as e:
            logging.error(f"Error starting Ollama service: {e}")

    try:
        thread = threading.Thread(target=run_service, daemon=True)
        thread.start()
        return "Ollama service is starting..."
    except Exception as e:
        logging.error(f"Error starting Ollama service thread: {e}")
        return f"Error starting Ollama service: {e}"

def log_loader():
    """Function to load log data."""
    return langchain.load_log_data()
