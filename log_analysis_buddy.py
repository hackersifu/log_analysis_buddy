# Log Analysis Buddy - AI Powered Log Analysis Helper

import openai
import os
import csv
import logging


analysis_file_var = 'random.txt'
analysis_file_location = os.getcwd()
analysis_file_full_path = os.path.join(analysis_file_location, analysis_file_var)


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


def log_analysis_buddy():
    """Function to run Log Analysis Buddy"""
    banner()
    print("Please enter the OpenAI API Key you would like to use for this session.")
    openai.api_key = input()
    print("Please provide the log file you would like to analyze. Please ensure that they are in CSV format and located in the same file as the log_analysis_buddy.py file.")
    log_file = input()
    log_location = os.getcwd()
    log_file_location = os.path.join(log_location, log_file)
    print("Please provide any additional context you'd like to provide to the Log Analysis Buddy.")
    additional_context_raw = input()
    additional_context = str(additional_context_raw)

    # Open the log file and read it into a variable for consumption by the OpenAI API
    try:
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
    log_analysis_buddy()
    file_cleanup()
    