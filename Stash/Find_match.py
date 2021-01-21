#Read logs to determine when you enter a match, leave a match and what class you're using
#To-do find latest match of class string
#To-do add loop in latest_file search so that everything else start ONLY when it finds a match
#https://thispointer.com/python-search-strings-in-a-file-and-get-line-numbers-of-lines-containing-the-string/
#https://stackoverflow.com/questions/39327032/how-to-get-the-latest-file-in-a-folder
#http://regex.inginf.units.it/#
#https://regex101.com/
import glob
import os
from datetime import datetime
import time
import datetime
import re
#list_of_files = glob.glob('C:\\Users\\romar\\AppData\\Local\\g3\\Saved\\Logs\\*') # * means all if need specific format then *.csv
list_of_files = glob.glob('H:\\Documents\\Programming\\Spellbreak\\Log_examples\\*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getmtime)
match_info={}
match_info['FileName'] = latest_file

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
                #print (list_of_results)
                #match_start_line_number=line_number[(len(line_number)-1)]
                #match_info['MatchStartLineNumber'] = match_start_line_number
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results


def find_match_start_time(match):
    #Convert match to string
    #regex_match_timestamp=re.findall(r'\d\d\d\d\.\d\d\.\d\d\-\d\d\.\d\d\.\d\d', str(match))
    regex_match_timestamp=re.findall(r'\d\d\d\d\.[^\]]*', str(match))
    #print (regex_match_timestamp)
    match_timestamp=''.join(regex_match_timestamp)
    #Add match_timestamp to dictionary
    match_info['MatchStart'] = match_timestamp
    #print (match_info)

def find_match_times(match):
    regex_match_timestamp=re.findall(r'\d\d\d\d\.[^\]]*', str(match))
    match_timestamp=''.join(regex_match_timestamp)
    match_info['MatchEnd'] = match_timestamp


def find_match_line_in_file(match, x):
    regex_match_line_number=re.findall(r'\(\w+,', str(match))
    match_line_number=''.join(regex_match_line_number)
    match_line_number = match_line_number.replace(',', '')
    match_line_number = match_line_number.replace('(', '')
    #print (regex_match_line_number)
    #Add match_timestamp to dictionary
    match_info['Match'+x+'LineNumber'] = match_line_number
    #print (match_info)

#Search for match start
matched_start_lines = search_string_in_file((latest_file), 'CONNECTING TO IP', 0)
latest_started_match=matched_start_lines[(len(matched_start_lines)-1)]
#print (latest_started_match)

#Conversions
find_match_times(latest_started_match)
find_match_line_in_file(latest_started_match, 'Start')

#Search for match end
matched_end_lines = search_string_in_file((latest_file), 'Received the final placement for the client in the match', 0)
#latest_ended_match=matched_end_lines[(len(matched_end_lines)-1)]
#find_match_times(latest_ended_match)
#find_match_line_in_file(latest_ended_match, 'End')


print (match_info)


