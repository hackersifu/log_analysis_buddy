import subprocess

def list_local_models():
    try:
        output = subprocess.check_output(["ollama", "list"], stderr=subprocess.STDOUT)
        return output.decode("utf-8")
    except Exception as e:
        return f"Error listing models: {e}"

def pull_model(model):
    try:
        output = subprocess.check_output(["ollama", "pull", model], stderr=subprocess.STDOUT)
        return output.decode("utf-8")
    except Exception as e:
        return f"Error pulling model {model}: {e}"
