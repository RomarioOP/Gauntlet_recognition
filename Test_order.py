import glob
import os
from datetime import datetime
import time
import datetime
import re


#Define global variables.
latest_file=""
match_found=False
#list_of_results=()
match_info={}
correct_order=False


def find_latest_log_file():
    list_of_files = glob.glob('H:\\Documents\\Programming\\Spellbreak\\Log_examples\\*') # * means all if need specific format then *.csv
    global latest_file
    latest_file = max(list_of_files, key=os.path.getmtime)
    match_info['FileName'] = latest_file
    print (latest_file)

def search_string_in_file(file_name, string_to_search, line_number):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    #line_number = 0
    global list_of_results
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
                #print("Match found. Resuming script.")
                global match_found
                match_found=True
                #print(list_of_results)
    return list_of_results

def find_match_times(match, order):
    regex_match_timestamp=re.findall(r'\d\d\d\d\.[^\]]*', str(match))
    match_timestamp=''.join(regex_match_timestamp)
    match_info['Match'+order] = match_timestamp


def find_match_line_in_file(match, x):
    regex_match_line_number=re.findall(r'\(\w+,', str(match))
    match_line_number=''.join(regex_match_line_number)
    match_line_number = match_line_number.replace(',', '')
    match_line_number = match_line_number.replace('(', '')
    #print (regex_match_line_number)
    #Add match_timestamp to dictionary
    match_info['Match'+x+'LineNumber'] = match_line_number
    #print (match_info)

def find_main_hand(file_name):
    for elem in file_name:
        #print('Line Number = ', elem[0], ' :: Line = ', elem[1])
        if "Pyromancer" in str(file_name):
            main_hand="fire"
        elif "Tempest" in str(file_name):
            main_hand="wind"
        elif "Conduit" in str(file_name):
            main_hand="lightning"
        elif "Stonehaper" in str(file_name):
            main_hand="stone"
        elif "Toxicologist" in str(file_name):
            main_hand="toxic"
        elif "Frostborn" in str(file_name):
            main_hand="ice"
        match_info['Main_hand'] = main_hand

#Find latest log file.
find_latest_log_file()

#Check if a matches have been found
while match_found==False:
    matched_start_lines = search_string_in_file((latest_file), 'CONNECTING TO IP', 0)
    time.sleep(1)

#If matches found then find last match.
latest_started_match=matched_start_lines[(len(matched_start_lines)-1)]
print (latest_started_match)

#Find match start time and match start line number and add to match information list.
find_match_times(latest_started_match, 'Start')
find_match_line_in_file(latest_started_match, 'Start')


#Now that a match has been found, the mainhand can be determined.
find_main_hand(latest_started_match)

#Now that main hand has been find: start loop to look for end of the match
#matched_end_lines = search_string_in_file((latest_file), 'Received the final placement for the client in the match', int(match_info['MatchStartLineNumber']))
# matched_end_lines = search_string_in_file((latest_file), 'Received the final placement for the client in the match', 0)
# latest_ended_match=matched_end_lines[(len(matched_end_lines)-1)]
# print(latest_ended_match)
# #Find match end time and match end line number 
# find_match_times(latest_ended_match, 'End')
# find_match_line_in_file(latest_ended_match, 'End')



#Print Match info
# print (match_info)
# if match_info['MatchStartLineNumber'] < match_info['MatchEndLineNumber']:
#     print("Order doesn't match. ")
# else:
#     print("Order matches.")

while correct_order==False:
    matched_end_lines = search_string_in_file((latest_file), 'Received the final placement for the client in the match', 0)
    latest_ended_match=matched_end_lines[(len(matched_end_lines)-1)]
    print(latest_ended_match)
    #Find match end time and match end line number 
    find_match_times(latest_ended_match, 'End')
    find_match_line_in_file(latest_ended_match, 'End')
    if match_info['MatchStartLineNumber'] > match_info['MatchEndLineNumber']:
        print("Order doesn't match.")
        time.sleep(3)
    else:
        print("Order matches.")
        #global correct_order
        correct_order=True
