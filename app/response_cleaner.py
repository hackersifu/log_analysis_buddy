#// Copyright 2025 Joshua McKiddy. All Rights Reserved.
#// SPDX-License-Identifier: Apache-2.0

import re
import logging
from llm_provider import get_default_provider
from langchain.prompts import PromptTemplate

def clean_response(text):
    """Function to clean the response and make it presentable in the UI."""
    cleaned_lines = []
    for line in text.splitlines():
        # Collapse multiple spaces into one per line.
        cleaned_line = " ".join(line.split())
        cleaned_lines.append(cleaned_line)
    cleaned_text = "\n".join(cleaned_lines)
    # Ensure Markdown headers have a single space after the '#' characters.
    cleaned_text = re.sub(r'^(#+)\s*', r'\1 ', cleaned_text, flags=re.MULTILINE)
    return cleaned_text

def refactor_response(provider_choice, api_key, model_string, cleaned_text):
    """
    Function to refactor the response with AI using LangChain's PromptTemplate.
    This formats the prompt nicely and then calls the provider's send_prompt method.
    """
    # Get the provider based on the selection.
    if provider_choice == "OpenAI":
        provider = get_default_provider("openai", api_key=api_key)
    else:
        provider = get_default_provider("ollama")
    
    # Use LangChain's PromptTemplate to structure the instruction.
    prompt_template = PromptTemplate(
        input_variables=["text"],
        template=(
            "Please refactor the following text into a well-structured report with clear headings, "
            "bullet points, and organized paragraphs. Fix any grammatical errors and remove unnecessary spaces.\n\n"
            "Text:\n{text}"
        )
    )
    
    # Format the prompt using the template.
    prompt_text = prompt_template.format(text=cleaned_text)
    logging.info("Refactoring response using LangChain prompt template...")
    
    try:
        # Call the provider's send_prompt with the formatted prompt.
        refactored_clean_response = provider.send_prompt(model_string, prompt_text)
    except Exception as exception_handle:
        logging.error(f"Error during LLM call in refactor_response: {exception_handle}")
        return None
    return refactored_clean_response
