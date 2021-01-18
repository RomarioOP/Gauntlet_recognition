import glob
import os
from datetime import datetime
import time
import datetime
import re
import win32api
from multiprocessing import Process
from threading import Thread
from yeelight import Bulb
from yeelight import LightType
import pyautogui
import json

#To-do: read user settings 
#Store session data in json file
#Ensure location to look for icons is always in folder where the script runs
#Add a "session" loop. This will enable the script to re-run when a match has been succesfully started and ended.






#print (os.getenv('LOCALAPPDATA'))
#Get latest log file
def find_latest_log_file():
    list_of_files = glob.glob(os.getenv('LOCALAPPDATA')+'\\g3\\Saved\\Logs\\*') # * means all if need specific format then *.csv
    global latest_file
    latest_file = max(list_of_files, key=os.path.getmtime)
    match_info['FileName'] = latest_file
    print (latest_file)

#Search if file contains a certain string
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
                #global match_found
                #match_found=True
                #print(list_of_results)
    return list_of_results

#Filter timestamp in a string based on regular expression
def find_match_times(match, order):
    regex_match_timestamp=re.findall(r'\d\d\d\d\.[^\]]*', str(match))
    match_timestamp=''.join(regex_match_timestamp)
    match_info['Match'+order] = match_timestamp

#Filter line number in a string based on regular expression
def find_match_line_in_file(match, x):
    regex_match_line_number=re.findall(r'\(\w+,', str(match))
    match_line_number=''.join(regex_match_line_number)
    match_line_number = match_line_number.replace(',', '')
    match_line_number = match_line_number.replace('(', '')

    match_info['Match'+x+'LineNumber'] = match_line_number
    #print (match_info)

#Find character class in string and assign the correct main hand element
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

#Define which off hand gauntlet is equiped
def gauntlet():
        global last_offhand
        global last_used_gauntlet
        global main_hand
        for i in elements:
            if pyautogui.locateOnScreen("H:\\Documents\\Programming\\Spellbreak\\Elements\\"+(i)+".png", region=(region), grayscale=True, confidence=0.8) != None:
                if last_offhand != i or last_offhand != last_used_gauntlet:
                    print("Switched from "+(last_offhand)+" to "+(i))                
                    rgb[(i)]()
                    last_offhand=(i)
                    last_used_gauntlet=(i)
                else:
                    print("Attacking with the same gauntlet as before. Skipping api call.")

#Check if a match has been started and finished
def find_completed_match():
    global should_restart
    global completed_match
    while completed_match==False:
        matched_end_lines = search_string_in_file((latest_file), 'Received the final placement for the client in the match', 0)
        if len(matched_end_lines) > 0:
            latest_ended_match=matched_end_lines[(len(matched_end_lines)-1)]
            print(latest_ended_match)
            #Find match end time and match end line number 
            find_match_times(latest_ended_match, 'End')
            find_match_line_in_file(latest_ended_match, 'End')
            if int(match_info['MatchStartLineNumber']) > int(match_info['MatchEndLineNumber']):
                print("Order doesn't match.")
                print (match_info['MatchStartLineNumber'])
                print (match_info['MatchEndLineNumber'])
                time.sleep(3)      
            else:
                print("Order matches.")
                find_match_times(latest_ended_match, 'End')
                find_match_line_in_file(latest_ended_match, 'End')
                print (match_info)
                print ("Session ended. Restarting new session.")
                time.sleep(5)
                completed_match=True
                should_restart=True
 
        else:
            time.sleep(3)

#Track mouse events
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


#Set rgb color codes
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
        global latest_started_match
        global session_match
        find_latest_log_file()
        matched_start_lines = search_string_in_file((latest_file), 'CONNECTING TO IP', 0)
        print("Looking for matches.")
        if  matched_start_lines:
            print ("Matches found. Filtering latest match.")
            latest_started_match=matched_start_lines[(len(matched_start_lines)-1)]
            #print (latest_started_match)
            print (session_match)
            if str(latest_started_match)==str(session_match):
                match_found==False
                return match_found
            else:
                session_match=latest_started_match
                match_found==True
                return match_found
            return match_found   
        else: 
            print ("No Matches found yet.")
            match_found==True
            return match_found
            time.sleep(1)
       

#Assign the region/location of the screen that has to be looked over to find the off hand
def set_gauntlet_position():
    global region
    with open('C:\\Users\\romar\\AppData\\Local\\g3\\Saved\\Config\\WindowsNoEditor\\GameUserSettings.ini') as f:
        if 'bSwapGauntletSlots=False' in f.read():
            region=(660,900,600,100)
        else:
            region=("tbd")

#Set Special keys
#To-do: get this info from ini file
global special_keys
special_keys = [0x01, 0x02]
special = {0x01: 'leftClick',
           0x02: 'rightClick',}
time.sleep(1)



#Start of script!
#Define global variables.
def start_complete_script():
    global latest_file
    global match_found
    global match_info
    global completed_match
    global last_used_gauntlet
    global last_offhand
    global main_hand
    global session_match
    global should_restart
    should_restart=False
    latest_file=""
    match_found=False
    match_info={}
    completed_match=False
    last_used_gauntlet=""
    last_offhand=""
    main_hand=""
    session_match=()
    #Find a started match in the latest log file. Function is a loop that resets the latest log file
    find_matches()
    print ("Matches found")
    #If matches found then find last match.
    #latest_started_match=matched_start_lines[(len(matched_start_lines)-1)]
    print ("Latest match:", latest_started_match)
    #Find match start time and match start line number and add to match information list.
    find_match_times(latest_started_match, 'Start')
    find_match_line_in_file(latest_started_match, 'Start')
    #Now that a match has been found, the mainhand can be determined.
    find_main_hand(latest_started_match)
    set_gauntlet_position()
    #Main hand found, setting rgb codes:
    set_rgb_codes()
    #Start checking for mouse input and start looking for end of match.
    t1 = Thread(target = find_completed_match)
    t2 = Thread(target = check_mouse_input)
    t1.start()
    t2.start()
    while True:
        if should_restart==False:
            print ("Match has not finished yet")
            time.sleep(3)
        else:
            print("writing json file")
            should_restart==True
            with open('result.json', 'w') as fp:
                json.dump (match_info, fp)
            break
    


# should_restart=True
# while should_restart==True:
#     if should_restart==True:
#         should_restart=False
#         start_complete_script()
#     else:
#         should_restart=True

should_restart=True    
while should_restart==True:
    start_complete_script()
    time.sleep(1)