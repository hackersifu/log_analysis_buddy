# Log Analysis Buddy - AI Powered Log Analysis Helper

import openai
import os
import csv
import logging
import inquirer
import json


def banner():
    """Function for Log Analysis Buddy banner"""
    print('''
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
''')
    
def prompt_questions():
    """Function for prompting questions to the user"""
    try:
        print("Please enter the OpenAI API Key you would like to use for this session.")
        openai.api_key = input()
        print("Please provide the log file you would like to analyze. Please ensure that they are in CSV format and located in the same file as the log_analysis_buddy.py file.")
        log_file = input()
        log_location = os.getcwd()
        log_file_location = os.path.join(log_location, log_file)
        print("Please provide any additional context you'd like to provide to the Log Analysis Buddy.")
        additional_context_raw = input()
        additional_context = str(additional_context_raw)
        model_selection = [
            inquirer.List('model',
                        message="Please select the model you would like to use for this session.",
                        choices=['text-davinci-002', 'gpt-3.5-turbo', 'gpt-4'],
                        ),
        ]
        # Data type conversion to JSON, then to string to get the model selection
        model_selection_answers = inquirer.prompt(model_selection)
        model_string_raw = json.dumps(model_selection_answers)
        model_json = json.loads(model_string_raw)
        model_string = (model_json["model"])
    except Exception as exception_handle:
        logging.error(exception_handle)
    return log_file_location, additional_context, model_string

def log_analysis_buddy(log_file_location, additional_context, model_string, analysis_file_var):
    """Function to run Log Analysis Buddy"""
    try:
        # text-davinci-002 model code
        if model_string == 'text-davinci-002':
            print(model_string + " selected.")
            with open(log_file_location, 'r') as csv_file:
                log_csv_reader = csv.reader(csv_file)
                with open(analysis_file_var, 'a') as analysis_file:
                    for line in log_csv_reader:
                        analysis_file.write(str(line))
                        analysis_file.write("\n")

            with open(analysis_file_var, 'r') as analysis_file:
                contents = analysis_file.read()

            response = openai.Completion.create(
                model="text-davinci-002",
                prompt="""
                Perform a detailed security analysis of these logs: 
                """
                + contents +
                """
                Use this additional context when performing the analysis: 
                """
                + additional_context,
                temperature=0.4,
                max_tokens=2000,
                top_p=1,
                frequency_penalty=-0.3,
                presence_penalty=0.3,
                stop=None
            )
            print(response["choices"][0]["text"])
        # gpt-3.5-turbo model code
        elif model_string == 'gpt-3.5-turbo':
            print(model_string + " selected.")
            with open(log_file_location, 'r') as csv_file:
                log_csv_reader = csv.reader(csv_file)
                with open(analysis_file_var, 'a') as analysis_file:
                    for line in log_csv_reader:
                        analysis_file.write(str(line))
                        analysis_file.write("\n")

            with open(analysis_file_var, 'r') as analysis_file:
                contents = analysis_file.read()

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                            {
                                "role": "user", 
                                "content": "Perform a detailed security analysis of these logs: " + contents + " Also, use this additional context when performing the analysis: " + additional_context
                            }
                        ],
                temperature=0.4,
                top_p=1,
                frequency_penalty=-0.3,
                presence_penalty=0.3,
                stop=None
            )
            print(response["choices"][0]["message"]["content"])
        # gpt-4 model code
        elif model_string == 'gpt-4':
            print(model_string + " selected.")
            with open(log_file_location, 'r') as csv_file:
                log_csv_reader = csv.reader(csv_file)
                with open(analysis_file_var, 'a') as analysis_file:
                    for line in log_csv_reader:
                        analysis_file.write(str(line))
                        analysis_file.write("\n")

            with open(analysis_file_var, 'r') as analysis_file:
                contents = analysis_file.read()

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                            {
                                "role": "user", 
                                "content": "Perform a detailed security analysis of these logs: " + contents + " Also, use this additional context when performing the analysis: " + additional_context
                            }
                        ],
                temperature=0.3,
                top_p=1,
                frequency_penalty=-0.6,
                presence_penalty=0.3,
                stop=None
            )
            print(response["choices"][0]["message"]["content"])

    except Exception as exception_handle:
        logging.error(exception_handle)

def file_cleanup():
    """Function to clean up the log file that was created for analysis"""
    try:
        print("")
        print("Cleanup of the log file that was created for analysis.")
        os.remove(analysis_file_var)
        print("Done.")
    except Exception as exception_handle:
        logging.error(exception_handle)


if __name__ == '__main__':
    """Main function for Log Analysis Buddy"""
    analysis_file_var = 'random.txt'
    analysis_file_location = os.getcwd()
    analysis_file_full_path = os.path.join(analysis_file_location, analysis_file_var)
    banner()
    log_file_location, additional_context, model_string = prompt_questions()
    log_analysis_buddy(log_file_location, additional_context, model_string, analysis_file_var)
    file_cleanup()
    