import ollama
import langchain
import json
import logging

ollama.api_url = "http://host.docker.internal:11434/api"

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
    
def pull_model(model_name):
    """Function to pull an Ollama model."""
    model = ollama.pull(model_name)
    return model

def log_loader():
    """Function to load log data."""
    return langchain.load_log_data()