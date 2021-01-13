#Read logs to determine when you enter a match, leave a match and what class you're using
#To-do find latest match of class string
#To-do add loop in latest_file search so that everything else start ONLY when it finds a match
#https://thispointer.com/python-search-strings-in-a-file-and-get-line-numbers-of-lines-containing-the-string/
#https://stackoverflow.com/questions/39327032/how-to-get-the-latest-file-in-a-folder
import glob
import os
from datetime import datetime
import time
list_of_files = glob.glob('C:\\Users\\romar\\AppData\\Local\\g3\\Saved\\Logs\\*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getmtime)
#print (latest_file)

def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    line_number = 0
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
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results

matched_lines = search_string_in_file((latest_file), 'CONNECTING TO IP')


#print(len(matched_lines)-1)

lastest_match=matched_lines[(len(matched_lines)-1)]



for elem in lastest_match:
    #print('Line Number = ', elem[0], ' :: Line = ', elem[1])
    if "Pyromancer" in str(lastest_match):
        main_hand="fire"
    elif "Tempest" in str(lastest_match):
        main_hand="wind"
    elif "Conduit" in str(lastest_match):
        main_hand="lightning"
    elif "Stoneshaper" in str(lastest_match):
        main_hand="stone"
    elif "Toxicologist" in str(lastest_match):
        main_hand="toxic"
    elif "Frostborn" in str(lastest_match):
        main_hand="ice"

print (lastest_match)
#print (main_hand)


try:
    time.strptime(str(lastest_match), "%Y.%m.%d-%H.%M.%S:%f")
    print ("found")
except ValueError:
    pass