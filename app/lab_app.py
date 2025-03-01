import streamlit as st
import os
import tempfile
import logging
import traceback
import re
import markdown
from log_analysis_buddy import analyze_logs, parse_log_file
from ollama_utils import list_local_models, pull_model, start_ollama_service
from response_cleaner import clean_response, refactor_response
import streamlit.components.v1 as components  # To render custom HTML

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Updated clean_response function:
# def clean_response(text):
#     """Function to clean the response and make it presentable in the UI."""
#     cleaned_lines = []
#     for line in text.splitlines():
#         # Collapse multiple spaces into one per line.
#         cleaned_line = " ".join(line.split())
#         cleaned_lines.append(cleaned_line)
#     cleaned_text = "\n".join(cleaned_lines)
#     # Ensure Markdown headers have a single space after the '#' characters.
#     cleaned_text = re.sub(r'^(#+)\s*', r'\1 ', cleaned_text, flags=re.MULTILINE)
#     return cleaned_text

st.title("Log Analysis Buddy - Scan Security Logs for Analysis and Actions")
st.write("Select an LLM provider, configure API details (if needed), manage Ollama models, attach a log file or enter its path, enter your prompt and additional context, then run the analysis.")

# # Custom CSS to style the output container
# st.markdown(
#     """
#     <style>
#     .output-markdown {
#         white-space: normal;
#         word-wrap: break-word;
#         background-color: white;
#         color: black;
#         padding: 1rem;
#         border: 1px solid #ccc;
#         border-radius: 5px;
#         margin-top: 1rem;
#         overflow-y: auto;
#         max-height: 600px;
#     }
#     .stMarkdown p {
#         margin: 0.5rem 0;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# Select LLM Provider
provider_choice = st.selectbox("Select LLM Provider", ["Ollama", "OpenAI"])

if provider_choice == "OpenAI":
    openai_api_key = st.text_input("Enter OpenAI API Key", type="password")
    if not openai_api_key:
        st.error("OpenAI API Key is required for OpenAI.")
else:
    ollama_api_url = st.text_input("Ollama API URL", value="http://localhost:11434/api")
    ollama_api_key = st.text_input("Ollama API Key (if required)", type="password")
    
    # Provide a button to start the Ollama service.
    if st.button("Start Ollama Service"):
        service_status = start_ollama_service()
        st.success(service_status)

    st.subheader("Ollama Model Management")
    if st.button("List Local Models"):
        output = list_local_models()
        st.text_area("Local Models", value=str(output), height=200)
    
    pull_model_choice = st.selectbox("Select a model to pull", ["llama3.2", "deepseek-r1", "gemma2:2b"])
    if st.button("Pull Selected Model"):
        pull_output = pull_model(pull_model_choice)
        st.text_area("Pull Output", value=pull_output, height=200)

# Log input method: either upload CSV or enter a file path.
log_input_method = st.radio("Select log input method", ["Upload CSV", "Enter file path"])
log_file_path = None
if log_input_method == "Upload CSV":
    uploaded_file = st.file_uploader("Upload Log CSV", type=["csv", "json", "txt"])
    if uploaded_file is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                log_file_path = tmp_file.name
        except Exception as e:
            st.error(f"Error saving uploaded file: {e}")
elif log_input_method == "Enter file path":
    file_path = st.text_input("Enter full path to log file", value="")
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
    # For Ollama, default to DeepSeek-R1 and Llama 3.2 per README.
    available_models = ["DeepSeek-R1", "llama3.2", "gemma2:2b"]
else:
    available_models = ["gpt-3.5-turbo", "gpt-4"]

model_choice = st.selectbox("Select Model", available_models)

if st.button("Run Analysis"):
    if (provider_choice == "OpenAI" and not openai_api_key) or log_file_path is None or not prompt_text:
        st.error("Please ensure all required fields are filled and a valid log file is provided.")
    else:
        st.info("Parsing log file...")
        try:
            parsed_logs = parse_log_file(log_file_path)
            st.subheader("Parsed Log Preview")
            st.text_area("Parsed Log Preview", value=parsed_logs, height=200, disabled=True)
            
            st.info("Running analysis...")
            response = analyze_logs(
                provider_choice=provider_choice,
                api_key=openai_api_key if provider_choice == "OpenAI" else None,
                log_file_path=log_file_path,
                additional_context=additional_context,
                model_string=model_choice
            )
            if response:
                st.success("Log analysis complete!")
                # Clean the response before rendering
                raw_cleaned = clean_response(response)
                key = openai_api_key if provider_choice == "OpenAI" else None
                refactored = refactor_response(provider_choice, key, model_choice, raw_cleaned)
                # Display the refactored response in a simple, scrollable text area.
                st.text_area("LLM Response", value=refactored, height=600, disabled=True)
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

