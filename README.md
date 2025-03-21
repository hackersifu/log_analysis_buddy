[![Twitter](https://img.shields.io/twitter/url?label=Follow%20Me%21&style=social&url=https%3A%2F%2Ftwitter.com%2Fdozercat31)](https://twitter.com/dozercat31)
![GitHub last commit](https://img.shields.io/github/last-commit/hackersifu/log_analysis_buddy)
![GitHub](https://img.shields.io/github/license/hackersifu/log_analysis_buddy)


# Log Analysis Buddy – AI-Powered Log Analysis Helper

Log Analysis Buddy is an open-source, AI-driven tool designed to help security analysts and incident responders perform comprehensive log analysis. By leveraging large language models (LLMs), it accepts log input (CSV or comma-delimited files) and provides deeper insights that augment an investigator’s workflow. 

This repository integrates features such as:

- **Multiple LLM Providers:** Support for providers like local Ollama models, or OpenAI.  
- **Flexible Log Formats:** Works primarily with CSV but can be adapted to handle JSON or other log types.  
- **Incident Response Focus:** Provides summarized, human-readable findings to expedite security investigations.  
- **Extensibility:** Built with Python (and optionally Streamlit for UI), making it straightforward to add advanced functionalities (e.g., correlation analysis, custom prompts).  

Through automating routine log parsing tasks and generating detailed, structured results, Log Analysis Buddy empowers responders to investigate incidents faster and produce more thorough reporting.

## Disclaimer
**2025-02-28: This project is currently in development and is a proof of concept. Additionally, you are responsible for any data that you provide to public LLMs via this project. This includes any logs that are provided, API keys, and any data via the context prompt.**

## Prerequisites
The following are prerequisites for using the Log Analysis Buddy:
- The ability to run Docker containers
- Log files in .csv (comma delimited) format, preferably
- An internet connection to download the initial models in the Docker
- The ability to run a local virtual environment (using venv)

## How to Use
Steps to use the Log Analysis Buddy:
1. After downloading the code, run the following command within the same directory as the code to build the Docker container:
```
docker build -t log_analysis_buddy .
```
If you're using an `apt` based environment, and you want to avoid mixing package installs, use a virtual environment with `venv` instead.
2. Run the Docker container
```
docker run -it -p 8501:8501 log_analysis_buddy
```
3. Access the container via the browser at `http://localhost:8501` to use the Log Analysis Buddy.
4. Select a model to use for the log analysis (available models are llama3.2, gamma2:2b and deepseek-r1)
![Alt Text](pics/model_selection.png)
5. Upload the log file you want to analyze and select "Run Analysis".
![Alt Text](pics/log_upload.png)


## Example Output
![Alt Text](pics/analysis_complete.png)
## Contributions & Feedback
For any contributions, feel free to create a [GitHub Pull Request](https://github.com/hackersifu/log_analysis_buddy/pulls). Additionally, you can use the Issues section to report bugs or submit feedback.

## License
This project is licensed under the Apache 2.0 licensing terms. Please see the LICENSE file for more information.
