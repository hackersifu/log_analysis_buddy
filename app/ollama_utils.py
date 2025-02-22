import ollama
import langchain

ollama.api_url = "http://host.docker.internal:11434/api"

def list_local_models():
    """Function to list local Ollama models."""
    local_models = ollama.list()
    return local_models

def pull_model(model_name):
    """Function to pull an Ollama model."""
    model = ollama.pull(model_name)
    return model

def log_loader():
    """Function to load log data."""
    return langchain.load_log_data()