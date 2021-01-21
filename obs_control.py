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
import threading
import inspect
import ctypes
import sys
import pathlib
from virtual_keystroke import *
#https://stackoverflow.com/questions/27050492/how-do-you-create-a-tkinter-gui-stop-button-to-break-an-infinite-loop
#https://stackoverflow.com/questions/3430372/how-do-i-get-the-full-path-of-the-current-files-directory
#https://imgur.com/a/7lb3wGf

#Store session data in json file
#Look for match cancel
#change look for match string to LogLoad: LogLoad: LoadMap: 23.109.51.20:8570

#Look for clash end of match
#[2021.01.16-14.03.27:969][246]LogGameMode:Display: Match State Changed from WaitingToStart to LeavingMap !json{"pid":13380,"env":"production","ver":"2.0.10050"}
#Create gui if needed

import asyncio
import simpleobsws

loop = asyncio.get_event_loop()
ws = simpleobsws.obsws(host='127.0.0.1', port=4444, password='MYSecurePassword', loop=loop) # Every possible argument has been passed, but none are required. See lib code for defaults.

async def make_request(element):
    await ws.connect() # Make the connection to OBS-Websocket
    result = await ws.call('GetVersion') # We get the current OBS version. More request data is not required
    print(result) # Print the raw json output of the GetVersion request
    await asyncio.sleep(0.1)
    data = {'scene-name': element}
    result = await ws.call('SetCurrentScene', data) # Make a request with the given data
    print(result)
    await ws.disconnect() # Clean things up by disconnecting. Only really required in a few specific situations, but good practice if you are done making requests or listening to events.


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
        global working_dir
        for i in elements:
            if pyautogui.locateOnScreen((working_dir)+"\\Elements\\"+(i)+".png", region=(region), grayscale=True, confidence=0.8) != None:
            #if pyautogui.locateOnScreen("H:\\Documents\\Programming\\Spellbreak\\Elements\\"+(i)+".png", region=(region), grayscale=True, confidence=0.8) != None:
                if last_offhand != i or last_offhand != last_used_gauntlet:
                    print("Switched from "+(last_offhand)+" to "+(i))                
                    rgb[(i)]()
                    last_offhand=(i)
                    last_used_gauntlet=(i)
                else:
                    print("Attacking with the same gauntlet as before. Skipping api call.")

#Check if a match has been started and finished
def find_completed_match():
    global completed_match
    global t1
    global t2
    while completed_match==False:
        matched_end_lines = search_string_in_file((latest_file), 'Received the final placement for the client in the match', 0)
        print("=========================================")
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
                print ("Session ended. Starting new session.")
                #terminate()
                completed_match=True
                time.sleep(5)
                start_complete_script()
                return
        else:
            time.sleep(3)

#Track mouse events
def check_mouse_input():
    global last_used_gauntlet
    global main_hand
    while completed_match==False:
        for i in range(1, 256):
            if win32api.GetAsyncKeyState(i):
                if i in special_keys:
                    if gauntlet_swap==False:
                        if i == 1:
                            print ("Attacking with main hand.")
                            if last_used_gauntlet==main_hand:
                                print("Light is already set to main hand settings. Skipping api call.")
                            else:
                                print("Activating color change.")
                                rgb[(main_hand)]()
                                last_used_gauntlet=main_hand
                        elif i == 2:
                            print ("Attacking with off hand.")
                            print ("Running gauntlet function.")
                            gauntlet()
                    else:
                        if i == 2:
                            print ("Attacking with main hand.")
                            if last_used_gauntlet==main_hand:
                                print("Light is already set to main hand settings. Skipping api call.")
                            else:
                                print("Activating color change.")
                                rgb[(main_hand)]()
                                last_used_gauntlet=main_hand
                        elif i == 1:
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
        'fire': lambda: print (pressHoldRelease("alt", "p")),
        'toxic': lambda: print (pressHoldRelease("alt", "i")),
        'ice': lambda: print (pressHoldRelease("alt", "o")),
        'wind': lambda: print (loop.run_until_complete(make_request('wind'))),
        'lightning': lambda: print (loop.run_until_complete(make_request('lightning'))),
        'stone': lambda: print (loop.run_until_complete(make_request('stone'))),
        'noodle': lambda: print (loop.run_until_complete(make_request('noodle')))
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
            print ("latest: " +str(latest_started_match))
            print ("session: " +str(session_match))
            print("checking if they are the same")
            time.sleep(1)
            if str(latest_started_match)==str(session_match):
                print("Old match, restarting function")
                time.sleep(1)
                continue
            else:
                print("this is a new match")
                session_match=(latest_started_match)
                print(session_match)
                match_found==True
                #Not sure if return below is required. Further testing needed
                return session_match
            continue 
        else: 
            print ("No Matches found yet.")
            time.sleep(1)
            continue
       
#Assign the region/location of the screen that has to be looked over to find the off hand
def set_gauntlet_position():
    global region
    global gauntlet_swap
    #with open('C:\\Users\\romar\\AppData\\Local\\g3\\Saved\\Config\\WindowsNoEditor\\GameUserSettings.ini') as f:
    with open(os.getenv('LOCALAPPDATA')+'\\g3\\Saved\\Config\\WindowsNoEditor\\GameUserSettings.ini') as f:
        if 'bSwapGauntletSlots=False' in f.read():
            region=(1150,915,65,70)
            gauntlet_swap=False
        else:
            region=(700,915,65,70)
            gauntlet_swap=True

#Set Special keys
def set_special_keys():
    global special_keys
    special_keys = [0x01, 0x02]
    special = {0x01: 'leftClick', 0x02: 'rightClick',}
    time.sleep(1)
   
#Full code execution!
def start_complete_script():
    global latest_file
    global match_found
    global match_info
    global completed_match
    global last_used_gauntlet
    global last_offhand
    global main_hand
    global session_match
    global t1
    global t2
    latest_file=""
    match_found=False
    match_info={}
    completed_match=False
    last_used_gauntlet=""
    last_offhand=""
    main_hand=""
    #Find a started match in the latest log file. Function is a loop that resets the latest log file
    find_matches()
    print ("Matches found")
    #If matches found then find last match.
    print ("Latest match:", latest_started_match)
    #Find match start time and match start line number and add to match information list.
    find_match_times(latest_started_match, 'Start')
    find_match_line_in_file(latest_started_match, 'Start')
    #Now that a match has been found, the mainhand can be determined.
    find_main_hand(latest_started_match)
    set_gauntlet_position()
    set_special_keys()
    #Main hand found, setting rgb codes:
    set_rgb_codes()
    #Start checking for mouse input and start looking for end of match.
    t1 = Thread(target = find_completed_match)
    t2 = Thread(target = check_mouse_input)
    t1.start()
    t2.start()
    # while True:
    #     if should_restart==False:
    #         print ("Match has not finished yet")
    #         time.sleep(3)
    #     else:
    #         print("writing json file")
    #         should_restart==True
    #         with open('result.json', 'w') as fp:
    #             json.dump (match_info, fp)
    #         break
    
global working_dir
working_dir=str(pathlib.Path(__file__).parent.absolute())
session_match=()
start_complete_script()
