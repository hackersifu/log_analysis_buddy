import streamlit as st
import os
import tempfile
import logging
import traceback
from log_analysis_buddy import analyze_logs
from ollama_utils import list_local_models, pull_model

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

st.title("Log Analysis Buddy - LLM Integration")
st.write("Select an LLM provider, configure API details (if needed), attach a log file or enter its path, enter your prompt and additional context, then run the analysis.")

# Select LLM Provider
provider_choice = st.selectbox("Select LLM Provider", ["Ollama", "OpenAI"])

if provider_choice == "OpenAI":
    openai_api_key = st.text_input("Enter OpenAI API Key", type="password")
    if not openai_api_key:
        st.error("OpenAI API Key is required for OpenAI.")
else:
    ollama_api_url = st.text_input("Ollama API URL", value="http://localhost:11434/api")
    ollama_api_key = st.text_input("Ollama API Key (if required)", type="password")

# Additional Ollama operations (only if provider is Ollama)
if provider_choice == "Ollama":
    st.subheader("Ollama Model Management")
    if st.button("List Local Models"):
        output = list_local_models()
        st.text_area("Local Models", value=output, height=200)
    
    pull_model_choice = st.selectbox("Select a model to pull", ["llama3.2", "deepseek-r1"])
    if st.button("Pull Selected Model"):
        pull_output = pull_model(pull_model_choice)
        st.text_area("Pull Output", value=pull_output, height=200)

# Log input method: either upload CSV or enter a file path.
log_input_method = st.radio("Select log input method", ["Upload CSV", "Enter file path"])
log_file_path = None
if log_input_method == "Upload CSV":
    uploaded_file = st.file_uploader("Upload Log CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                log_file_path = tmp_file.name
        except Exception as e:
            st.error(f"Error saving uploaded file: {e}")
elif log_input_method == "Enter file path":
    file_path = st.text_input("Enter full path to log CSV file", value="")
    if file_path:
        if os.path.exists(file_path):
            log_file_path = file_path
        else:
            st.error("File not found at the provided path.")

# Prompt and Additional Context
prompt_text = st.text_area("Enter your prompt:", "Analyze the following logs for security anomalies.")
additional_context = st.text_area("Additional Context (optional):", "Enter any extra details here.")

# Model selection based on provider.
if provider_choice.lower() == "ollama":
    # For Ollama, default to DeepSeek-R1 and Llama 3.1 per README.
    available_models = ["DeepSeek-R1", "Llama 3.1"]
else:
    available_models = ["gpt-3.5-turbo", "gpt-4"]

model_choice = st.selectbox("Select Model", available_models)

if st.button("Run Analysis"):
    if (provider_choice == "OpenAI" and not openai_api_key) or log_file_path is None or not prompt_text:
        st.error("Please ensure all required fields are filled and a valid log file is provided.")
    else:
        st.info("Running analysis...")
        try:
            response = analyze_logs(
                provider_choice=provider_choice,
                api_key=openai_api_key if provider_choice == "OpenAI" else None,
                log_file_path=log_file_path,
                additional_context=additional_context,
                model_string=model_choice
            )
            if response:
                st.subheader("LLM Response")
                st.code(response)
            else:
                st.error("Log analysis failed. Check logs for details.")
        except Exception as e:
            tb = traceback.format_exc()
            st.error(f"Log analysis failed with error: {e}\n\nTraceback:\n{tb}")
        finally:
            if log_input_method == "Upload CSV" and log_file_path:
                try:
                    os.remove(log_file_path)
                except Exception as e:
                    st.error(f"Error cleaning up temporary file: {e}")

