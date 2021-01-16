from datetime import datetime
import glob
import os
import time
import re


#Define global variables.
latest_file=""
match_found=False

def find_latest_log_file():
    list_of_files = glob.glob('H:\\Documents\\Programming\\Spellbreak\\Log_examples\\*') # * means all if need specific format then *.csv
    global latest_file
    latest_file = max(list_of_files, key=os.path.getmtime)
    print (latest_file)

def search_string_in_file(file_name, string_to_search, line_number):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    #line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))
                print (list_of_results)
                #match_start_line_number=line_number[(len(line_number)-1)]
                #match_info['MatchStartLineNumber'] = match_start_line_number
    # Return list of tuples containing line numbers and lines where string is found
                print("Match found. Resuming script.")
                global match_found
                match_found=True
    return list_of_results



#Find latest log file
find_latest_log_file()

#
while match_found==False:
    search_string_in_file((latest_file), 'CONNECTING TO IP', 0)
    time.sleep(5)

