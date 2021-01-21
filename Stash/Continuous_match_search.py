from datetime import datetime
import glob
import os
import time
import re
#First find latest log file
#Compare if that file is created before or after this script has started.
# datetime object containing current date and time
now = datetime.now()
current_time = now.strftime("%Y.%m.%d-%H.%M.%S")
#print(current_time)




global latest_file
global start_found
 
latest_file=""

def find_latest_log_file():
    list_of_files = glob.glob('H:\\Documents\\Programming\\Spellbreak\\Log_examples\\*') # * means all if need specific format then *.csv
    global latest_file
    latest_file = max(list_of_files, key=os.path.getmtime)
    print (latest_file)


def search_string_in_file(file_name, string_to_search, line_number, order):
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
                #print (list_of_results)
                #match_start_line_number=line_number[(len(line_number)-1)]
                #match_info['MatchStartLineNumber'] = match_start_line_number
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results





#Find latest log file
find_latest_log_file()

#Check if a match has started in that file
start_found=False
while True:
    # matched_start_lines=search_string_in_file((latest_file), 'CONNECTING TO IP', 0)
    # print (matched_start_lines)
    # if 'CONNECTING TO IP' in matched_start_lines:
    #     match_found=True
    #     print ('Match found!')
    #     time.sleep(5)
    # else:
    #     matched_start_lines=False
    #     print ("No match found yet.")
    #     time.sleep(5)

#print (matched_start_lines)
#latest_started_match=matched_start_lines[(len(matched_start_lines)-1)]
#print (latest_started_match)
#Find the last started match in match_start_lines
#Find a started match