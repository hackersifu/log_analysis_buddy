#// Copyright 2025 Joshua McKiddy. All Rights Reserved.
#// SPDX-License-Identifier: Apache-2.0

import streamlit as st
import os
import tempfile
import logging
import traceback
import re

from log_analysis_buddy import analyze_logs, parse_log_file
from ollama_utils import list_local_models, pull_model, start_ollama_service
from response_cleaner import clean_response, refactor_response

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

st.title("Log Analysis Buddy - Scan Security Logs for Analysis and Actions")
st.write(
    "Select an LLM provider, configure API details (if needed), manage Ollama models, "
    "attach a log file or enter its path, enter your prompt and additional context, then run the analysis."
)

provider_choice = st.selectbox("Select LLM Provider", ["Ollama", "OpenAI"])

if provider_choice == "OpenAI":
    openai_api_key = st.text_input("Enter OpenAI API Key", type="password")
    if not openai_api_key:
        st.error("OpenAI API Key is required for OpenAI.")
else:
    ollama_api_url = st.text_input("Ollama API URL", value="http://localhost:11434/api")
    ollama_api_key = st.text_input("Ollama API Key (if required)", type="password")

    if st.button("Start Ollama Service"):
        service_status = start_ollama_service()
        st.success(service_status)

    st.subheader("Ollama Model Management")
    if st.button("List Local Models"):
        output = list_local_models()
        st.text_area("Local Models", value=str(output), height=200)

    pull_model_choice = st.selectbox("Select a model to pull", ["gemma2:2b", "gemma3:1b", "llama3.2", "deepseek-r1"])

    if st.button("Pull Selected Model"):
        pull_output = pull_model(pull_model_choice)
        st.text_area("Pull Output", value=pull_output, height=200)

# Log input method
log_input_method = st.radio("Select log input method", ["Upload CSV", "Enter file path"])
log_file_path = None

if log_input_method == "Upload CSV":
    uploaded_file = st.file_uploader("Upload Log CSV", type=["csv", "json", "txt"])
    if uploaded_file:
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

# Model selection
if provider_choice.lower() == "ollama":
    available_models = ["gemma2:2b", "gemma3:1b", "DeepSeek-R1", "llama3.2"]
else:
    available_models = ["gpt-3.5-turbo", "gpt-4"]

model_choice = st.selectbox("Select Model", available_models)

if st.button("Run Analysis"):
    if (provider_choice == "OpenAI" and not openai_api_key) or (log_file_path is None) or (not prompt_text):
        st.error("Please provide required fields (API key if OpenAI, valid log file, and prompt).")
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
                # 1) Clean the raw response
                raw_cleaned = clean_response(response)

                # 2) Refactor the cleaned response to produce well-formatted Markdown
                key = openai_api_key if provider_choice == "OpenAI" else None
                refactored = refactor_response(provider_choice, key, model_choice, raw_cleaned)

                if refactored:
                    # Render as Markdown. unsafe_allow_html=False ensures we interpret bullet points properly.
                    st.markdown(refactored, unsafe_allow_html=False)
                else:
                    # If refactoring fails, fallback
                    st.text_area("LLM Response (fallback)", value=raw_cleaned, height=600, disabled=True)
            else:
                st.error("Log analysis failed. Check logs for details.")

        except Exception as e:
            tb = traceback.format_exc()
            st.error(f"Log analysis failed with error: {e}\n\nTraceback:\n{tb}")
        finally:
            # Cleanup
            if log_input_method == "Upload CSV" and log_file_path:
                try:
                    os.remove(log_file_path)
                except Exception as e:
                    st.error(f"Error cleaning up temporary file: {e}")
