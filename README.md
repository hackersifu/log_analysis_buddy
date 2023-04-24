# Log Analysis Buddy - AI Powered Log Analysis Helper
The Log Analysis Buddy is an AI powered log analysis helper that can be used to help analysts perform log analysis. The Log analysis Buddy uses OpenAI to receive log input (in .csv, or comma delimited, format) from an incident responder, to perform additional analysis for the responder. This analysis can be used to augment the responder's investigation, to provide thourogh results for reporting.

## Prerequisites
The following are prerequisites for using the Log Analysis Buddy:
- An OpenAPI key (from creating an OpenAI account)
- Log files in .csv format (comma delimited), placed in the same location as the log_analysis_buddy.py file
- Python 3.7 or higher
- OpenAI Python library (installed via pip)

## How to Use
Steps to use the Log Analysis Buddy:
1. Install the OpenAI Python library using pip (if not installed already).
'''
pip install openai
OR
pip3 install openai
'''
2. Place the log_analysis_buddy.py file in the same location as the log files to be analyzed.
3. Run the log_analysis_buddy.py file using Python 3.7 or higher.
'''
python log_analysis_buddy.py
OR
python3 log_analysis_buddy.py
'''
4. Enter the OpenAI API key when prompted.
5. Enter the name of the log file to be analyzed (including the .csv extension).
6. Enter context for the analysis (i.e. "Look for malicious trends.").

## Example Output
'''
Possible malicious trends:
-A large number of events coming from a single IP address, particularly one that is not within the AWS infrastructure. This could indicate someone attempting to access AWS resources maliciously.
'''

## Contributions & Feedback
For any contributions, feel free to create a [GitHub Pull Request](https://github.com/hackersifu/log_analysis_buddy/pulls). Additionally, you can use the Issues section to report bugs or submit feedback.

## License
This project is licensed under the Apache 2.0 licensing terms.
