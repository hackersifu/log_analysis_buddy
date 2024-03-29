[![Twitter](https://img.shields.io/twitter/url?label=Follow%20Me%21&style=social&url=https%3A%2F%2Ftwitter.com%2Fdozercat31)](https://twitter.com/dozercat31)
![GitHub last commit](https://img.shields.io/github/last-commit/hackersifu/log_analysis_buddy)
![GitHub](https://img.shields.io/github/license/hackersifu/log_analysis_buddy)


# Log Analysis Buddy - AI Powered Log Analysis Helper
The Log Analysis Buddy is an AI powered log analysis helper that can be used to help analysts perform log analysis. The Log analysis Buddy uses OpenAI to receive log input (in .csv, or comma delimited, format) from an incident responder, to perform additional analysis for the responder. This analysis can be used to augment the responder's investigation, to provide thourogh results for reporting.

## Disclaimer
**2023-04-24: This project is currently in development and is a proof of concept. Additionally, you are responsible for any data that you provide to OpenAI via this project. Please ensure that you are not providing any sensitive data to OpenAI via this project. This includes any logs that are provided, API keys, and any data via the context prompt.**

## Prerequisites
The following are prerequisites for using the Log Analysis Buddy:
- An OpenAPI key (from creating an OpenAI account)
- Log files in .csv format (comma delimited), placed in the same location as the log_analysis_buddy.py file
- Python 3.9 or higher
- Python packages contained in the requirements.txt file (installed via pip)
  - openai (and various dependent packages for this module)
  - inquirer (and various dependent packages for this module)

## How to Use
Steps to use the Log Analysis Buddy:
1. Install the dependencies within the requirements file using pip (if not installed already).
```
pip install -r requirements.txt
OR
pip3 install -r requirements.txt
```
If you're using an `apt` based environment, and you want to avoid mixing package installs, use a virtual environment with `venv` instead.
2. Place the log_analysis_buddy.py file in the same location as the log files to be analyzed.
3. Run the log_analysis_buddy.py file using Python 3.7 or higher.
```
python log_analysis_buddy.py
OR
python3 log_analysis_buddy.py
```
4. Enter the OpenAI API key when prompted.
5. Enter the name of the log file to be analyzed (including the .csv extension).
6. Enter context for the analysis (i.e. "Look for malicious trends.").
7. NEW! Select the model to use for the analysis (i.e. gpt-3.5-turbo) from the provided list.

## Example Input
```
python log_analysis_buddy.py

____________________
    _
    /
---/-------__----__-
  /      /   ) /   )
_/____/_(___/_(___/_
                 /
             (_ /
____________________________________________
    __
    / |                /              ,
---/__|----__----__---/---------__-------__-
  /   |  /   ) /   ) /   /   / (_ ` /   (_ `
_/____|_/___/_(___(_/___(___/_(__)_/___(__)_
                           /
                       (_ /
_______________________________________
    ____
    /   )               /       /
---/__ /------------__-/----__-/-------
  /    )   /   /  /   /   /   /   /   /
_/____/___(___(__(___/___(___/___(___/_
                                    /
                                (_ /
        Joshua "DozerCat" McKiddy
        Twitter - @dozercat31

Please enter the OpenAI API Key you would like to use for this session.
sk-addyourkeyhere
Please provide the log file you would like to analyze. Please ensure that they are in CSV format and located in the same file as the log_analysis_buddy.py file.
test_logs.csv
Please provide any additional context you'd like to provide to the Log Analysis Buddy.
Look for malicious trends.
[?] Please select the model you would like to use for this session.: gpt-3.5-turbo
   text-davinci-002
 > gpt-3.5-turbo
```

## Example Output
```
Possible malicious trends:
-A large number of events coming from a single IP address, particularly one that is not 
within the AWS infrastructure. This could indicate someone attempting to access 
AWS resources maliciously.
```

## Contributions & Feedback
For any contributions, feel free to create a [GitHub Pull Request](https://github.com/hackersifu/log_analysis_buddy/pulls). Additionally, you can use the Issues section to report bugs or submit feedback.

## License
This project is licensed under the Apache 2.0 licensing terms. Please see the LICENSE file for more information.
