import glob
import os
from datetime import datetime
import time
import datetime
import re
import win32api
import time
from multiprocessing import Process
from threading import Thread
from yeelight import Bulb
from yeelight import LightType
import win32api
import time
import pyautogui
import yeelight
from yeelight import Bulb
from yeelight import LightType
import glob
import os

#Define global variables.
latest_file=""
match_found=False
match_info={}
completed_match=False
last_used_gauntlet=""
last_offhand=""
sequence_completed=False
main_hand=""





def find_latest_log_file():
    list_of_files = glob.glob('C:\\Users\\romar\\AppData\\Local\\g3\\Saved\\Logs\\*') # * means all if need specific format then *.csv
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
    global main_hand
    for elem in file_name:
        #print('Line Number = ', elem[0], ' :: Line = ', elem[1])
        if "Pyromancer" in str(file_name):
            main_hand="fire"
        elif "Tempest" in str(file_name):
            main_hand="wind"
        elif "Conduit" in str(file_name):
            main_hand="lightning"
        elif "Stoneshaper" in str(file_name):
            main_hand="stone"
        elif "Toxicologist" in str(file_name):
            main_hand="toxic"
        elif "Frostborn" in str(file_name):
            main_hand="ice"
        #match_info['Main_hand'] = main_hand
    print ("Main hand found: "+ main_hand)

def gauntlet():
        global last_offhand
        global last_used_gauntlet
        global main_hand
        for i in elements:
            if pyautogui.locateOnScreen("H:\\Documents\\Programming\\Spellbreak\\Elements\\"+(i)+".png", region=(660,900,600,100), grayscale=True, confidence=0.8) != None:
                if last_offhand != i or last_offhand != last_used_gauntlet:
                    print("Switched from "+(last_offhand)+" to "+(i))                
                    rgb[(i)]()
                    last_offhand=(i)
                    last_used_gauntlet=(i)
                else:
                    print("Attacking with the same gauntlet as before. Skipping api call.")

def find_completed_match():
    global completed_match
    global sequence_completed
    while completed_match==False:
        matched_end_lines = search_string_in_file((latest_file), 'Received the final placement for the client in the match', 0)
        if len(matched_end_lines) > 0:
            latest_ended_match=matched_end_lines[(len(matched_end_lines)-1)]
            print(latest_ended_match)
            #Find match end time and match end line number 
            find_match_times(latest_ended_match, 'End')
            find_match_line_in_file(latest_ended_match, 'End')
            if match_info['MatchStartLineNumber'] < match_info['MatchEndLineNumber']:
                print("Order doesn't match.")
                time.sleep(3)      
            else:
                print("Order matches.")
                find_match_times(latest_ended_match, 'End')
                find_match_line_in_file(latest_ended_match, 'End')
                completed_match=True
                sequence_completed=True
                print (match_info)
        else:
            time.sleep(3)

def check_mouse_input():
    global completed_match
    global last_used_gauntlet
    global main_hand
    while completed_match==False:
        for i in range(1, 256):
            if win32api.GetAsyncKeyState(i):
                if i in special_keys:
                    ### Main hand code
                    if i == 1:
                        print ("Attacking with main hand.")
                        if last_used_gauntlet==main_hand:
                            print("Light is already set to main hand settings. Skipping api call.")
                        else:
                            print("Activating color change.")
                            rgb[(main_hand)]()
                            last_used_gauntlet=main_hand
                    ### End main hand code
                    elif i == 2:
                        print ("Attacking with off hand.")
                        print ("Running gauntlet function.")
                        gauntlet()

    time.sleep(0.3)

def set_rgb_codes():
    global main_hand
    global bulb
    global rgb
    bulb = Bulb("192.168.178.15")
    rgb = {
        'fire': lambda: print (bulb.set_rgb(255,0,0)),
        'toxic': lambda: print (bulb.set_rgb(0,255,0)),
        'ice': lambda: print (bulb.set_rgb(0,0,255)),
        'wind': lambda: print (bulb.set_rgb(255,255,0)),
        'lightning': lambda: print (bulb.set_rgb(127,0,255)),
        'stone': lambda: print (bulb.set_rgb(153,76,8)),
        'noodle': lambda: print (bulb.set_rgb(255,20,147))
    }
    all_elements = ["wind", "toxic", "ice", "fire", "stone" ,"lightning", "noodle"]
    global elements
    elements = []
    for i in all_elements:
        elements.append(i)
    elements.remove(main_hand)
    
   
#Check if a matches have been found
def find_matches():
    while match_found==False:
        global matched_start_lines
        find_latest_log_file()
        matched_start_lines = search_string_in_file((latest_file), 'CONNECTING TO IP', 0)
        print("Looking for matches.")
        time.sleep(1)

#Set Special keys
#To-do: get this info from ini file
global special_keys
special_keys = [0x01, 0x02]
special = {0x01: 'leftClick',
           0x02: 'rightClick',}
time.sleep(1)
           
#Find a started match in the latest log file. Function is a loop that resets the latest log file
find_matches()
print ("Matches found")
#If matches found then find last match.
latest_started_match=matched_start_lines[(len(matched_start_lines)-1)]
print ("Latest match:", latest_started_match)
#Find match start time and match start line number and add to match information list.
find_match_times(latest_started_match, 'Start')
find_match_line_in_file(latest_started_match, 'Start')
#Now that a match has been found, the mainhand can be determined.
find_main_hand(latest_started_match)
#Main hand found, setting rgb codes:
set_rgb_codes()

#Start checking for mouse input and start looking for end of match.
t1 = Thread(target = find_completed_match)
t2 = Thread(target = check_mouse_input)
t1.start()
t2.start()
