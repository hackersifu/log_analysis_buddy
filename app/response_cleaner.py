#// Copyright 2025 Joshua McKiddy. All Rights Reserved.
#// SPDX-License-Identifier: Apache-2.0

import re
import logging
from llm_provider import get_default_provider
from langchain.prompts import PromptTemplate

def clean_response(text):
    """Function to clean up the response text from the LLM."""

    cleaned_lines = []
    for line in text.splitlines():
        # Collapse multiple spaces into one per line
        cleaned_line = " ".join(line.split())
        cleaned_lines.append(cleaned_line)
    cleaned_text = "\n".join(cleaned_lines)
    # Need to fix
    cleaned_text = re.sub(r'^(#+)\s*', r'\1 ', cleaned_text, flags=re.MULTILINE)
    return cleaned_text

def refactor_response(provider_choice, api_key, model_string, cleaned_text):
    """Function to refactor the cleaned response into valid Markdown using the LangChain LLM."""
    if provider_choice == "OpenAI":
        provider = get_default_provider("openai", api_key=api_key)
    else:
        provider = get_default_provider("ollama")
    prompt_template = PromptTemplate(
        input_variables=["text"],
        template=(
            "Refactor the following text into valid Markdown with:\n"
            "- Proper headings (e.g., '# Overview', '## Observations')\n"
            "- Bullet points (using '- ' or '* ')\n"
            "- Paragraphs separated by blank lines\n"
            "- Make sure to include blank lines between paragraphs and each bullet point on its own line\n"
            "Fix grammatical errors, remove extra spacing, but do NOT remove essential content.\n\n"
            "Text to refactor:\n{text}"
        )
    )
    prompt_text = prompt_template.format(text=cleaned_text)
    logging.info("Refactoring response using LangChain prompt template...")

    try:
        # Send to the LLM
        refactored_clean_response = provider.send_prompt(model_string, prompt_text)
    except Exception as e:
        logging.error(f"Error during LLM call in refactor_response: {e}")
        return None

    return refactored_clean_response
