#// Copyright 2025 Joshua McKiddy. All Rights Reserved.
#// SPDX-License-Identifier: Apache-2.0

import requests
import logging
import json
import re

class BaseLLMProvider:
    def get_available_models(self):
        raise NotImplementedError

    def send_prompt(self, model, prompt, additional_context=""):
        raise NotImplementedError

class OllamaProvider(BaseLLMProvider):
    def __init__(self, api_url="http://localhost:11434/api", api_key=None):
        self.api_url = api_url
        self.api_key = api_key

    def get_available_models(self):
        return ["Ollama-gpt-4", "Ollama-gpt-3.5"]

    def send_prompt(self, model, prompt, additional_context=""):
        payload = {
            "model": model,
            "prompt": prompt,
            "additional_context": additional_context
        }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        url = f"{self.api_url}/generate"
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            fragments = []
            for line in response.text.strip().splitlines():
                if line.strip():
                    try:
                        data = json.loads(line)
                        part = data.get("response", "")

                        fragments.append(part)
                    except Exception as e:
                        logging.error(f"Error parsing line: {line} | {e}")

            # JOIN WITH NEWLINES to preserve headings/bullets from the LLM
            final_response = "\n".join(fragments)

            return final_response.strip()

        else:
            raise Exception(f"Ollama API error: {response.status_code} {response.text}")



class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key):
        import openai
        self.api_key = api_key
        openai.api_key = api_key

    def get_available_models(self):
        return ["gpt-3.5-turbo", "gpt-4"]

    def send_prompt(self, model, prompt, additional_context=""):
        import openai
        full_prompt = f"{prompt}\nAdditional Context: {additional_context}"
        if model.startswith("gpt-"):
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.4,
                max_tokens=1500
            )
            return response["choices"][0]["message"]["content"]
        else:
            response = openai.Completion.create(
                model=model,
                prompt=full_prompt,
                temperature=0.4,
                max_tokens=1500
            )
            return response["choices"][0]["text"]

def get_default_provider(provider_name="ollama", **kwargs):
    if provider_name.lower() == "ollama":
        return OllamaProvider(
            api_url=kwargs.get("api_url", "http://localhost:11434/api"),
            api_key=kwargs.get("api_key")
        )
    elif provider_name.lower() == "openai":
        return OpenAIProvider(api_key=kwargs["api_key"])
    else:
        raise ValueError(f"Unsupported provider: {provider_name}")
