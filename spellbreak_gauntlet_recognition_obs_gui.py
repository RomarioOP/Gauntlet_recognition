import glob
import os
from datetime import datetime
import time
import re
from multiprocessing import Process
from threading import Thread
import pyautogui
import json
import threading
import inspect
import ctypes
import sys
import pathlib
import win32api
import Yeelight_control
import Obs_hotkeys
import tkinter
import _tkinter
from tkinter import *
from _tkinter import *
from subprocess import Popen
import virtual_keystroke
#https://stackoverflow.com/questions/27050492/how-do-you-create-a-tkinter-gui-stop-button-to-break-an-infinite-loop
#https://stackoverflow.com/questions/3430372/how-do-i-get-the-full-path-of-the-current-files-directory
#https://imgur.com/a/SiqFu6S
#Store session data in json file
#Look for match cancel
#change look for match string to LogLoad: LogLoad: LoadMap: 23.109.51.20:8570

#Look for clash end of match
#[2021.01.16-14.03.27:969][246]LogGameMode:Display: Match State Changed from WaitingToStart to LeavingMap !json{"pid":13380,"env":"production","ver":"2.0.10050"}
#Create gui if needed

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
    with open(file_name, 'r', encoding='utf8') as read_obj:
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

#Find which off hand is equipped
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
                    Obs_hotkeys.gauntlets[(i)]()
                    last_offhand=(i)
                    last_used_gauntlet=(i)
                else:
                    print("Attacking with the same gauntlet as before. Skipping api call.")

#Check if a match has been started and finished
def find_completed_match():
    global completed_match
    while completed_match==False:
#===============================================================================================================================#
# Match end search  (Battleroyale mode)      
#===============================================================================================================================#
        matched_end_lines = search_string_in_file((latest_file), 'Received the final placement for the client in the match', 0)
        print("Checking for finished match")
        if len(matched_end_lines) > 0:
            latest_ended_match=matched_end_lines[(len(matched_end_lines)-1)]
            #print(latest_ended_match)
            #Find match end time and match end line number 
            find_match_times(latest_ended_match, 'End')
            find_match_line_in_file(latest_ended_match, 'End')
            if int(match_info['MatchStartLineNumber']) > int(match_info['MatchEndLineNumber']):
                # print("Order doesn't match.")
                # print (match_info['MatchStartLineNumber'])
                # print (match_info['MatchEndLineNumber'])
                #time.sleep(3)
                pass      
            else:
                #print("Order matches.")
                #find_match_times(latest_ended_match, 'End')
                #find_match_line_in_file(latest_ended_match, 'End')
                match_info.pop('MatchCancel', None)
                match_info.pop('MatchCancelLineNumber', None)
                print (match_info)
                # with open((working_dir)+"\\Match_results\\result_"+time.strftime("%Y%m%d")+".log", 'a') as fp:
                #     fp.write(f'\n {match_info}')
                # print ("Session ended. Starting new session.")
                Obs_hotkeys.gauntlets["default"]()
                #terminate()
                completed_match=True
                time.sleep(3)
                start_complete_script()
                return
#===============================================================================================================================#
# Match cancel search     Works for canceled matches and Clash matches.               
#===============================================================================================================================#
        matched_cancel_lines = search_string_in_file((latest_file), 'StartLoadingLevel /Game/Maps/MainMenu/MainMenu_Root', 0)
        print("Checking canceled match")
        if len(matched_cancel_lines) > 0:
            latest_cancel_match=matched_cancel_lines[(len(matched_cancel_lines)-1)]
            #print(latest_ended_match)
            #Find match end time and match end line number 
            find_match_times(latest_cancel_match, 'Cancel')
            find_match_line_in_file(latest_cancel_match, 'Cancel')
            if int(match_info['MatchStartLineNumber']) > int(match_info['MatchCancelLineNumber']):
                # print("Order doesn't match.")
                # print (match_info['MatchStartLineNumber'])
                # print (match_info['MatchEndLineNumber'])
                pass      
            else:
                #print("Order matches.")
                #find_match_times(latest_ended_match, 'End')
                #find_match_line_in_file(latest_ended_match, 'End')
                match_info.pop('MatchEnd', None)
                match_info.pop('MatchEndLineNumber', None)
                # print (match_info)
                # with open((working_dir)+"\\Match_results\\result_"+time.strftime("%Y%m%d")+".log", 'a') as fp:
                #     fp.write(f'\n {match_info}')
                print ("Session ended. Starting new session.")
                Obs_hotkeys.gauntlets["default"]()
                #terminate()
                completed_match=True
                time.sleep(3)
                start_complete_script()
                return
#===============================================================================================================================#
# Match end search  (Clash mode)      
#===============================================================================================================================#
        # matched_end_lines = search_string_in_file((latest_file), 'Starting load of match end screen', 0)
        # print("Checking for finished match")
        # if len(matched_end_lines) > 0:
        #     latest_ended_match=matched_end_lines[(len(matched_end_lines)-1)]
        #     #print(latest_ended_match)
        #     #Find match end time and match end line number 
        #     find_match_times(latest_ended_match, 'End')
        #     find_match_line_in_file(latest_ended_match, 'End')
        #     if int(match_info['MatchStartLineNumber']) > int(match_info['MatchEndLineNumber']):
        #         # print("Order doesn't match.")
        #         # print (match_info['MatchStartLineNumber'])
        #         # print (match_info['MatchEndLineNumber'])
        #         #time.sleep(3)
        #         pass      
        #     else:
        #         #print("Order matches.")
        #         #find_match_times(latest_ended_match, 'End')
        #         #find_match_line_in_file(latest_ended_match, 'End')
        #         match_info.pop('MatchCancel', None)
        #         match_info.pop('MatchCancelLineNumber', None)
        #         print (match_info)
        #         print ("Session ended. Starting new session.")
        #         #terminate()
        #         completed_match=True
        #         time.sleep(5)
        #         start_complete_script()
        #         return
        time.sleep(5)

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
                                Obs_hotkeys.gauntlets[(main_hand)]()
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
                                Obs_hotkeys.gauntlets[(main_hand)]()
                                last_used_gauntlet=main_hand
                        elif i == 1:
                            print ("Attacking with off hand.")
                            print ("Running gauntlet function.")
                            gauntlet()                    
        time.sleep(0.3)

def set_elements():
    all_elements = ["wind", "toxic", "ice", "fire", "stone" ,"lightning", "noodle"]
    global elements
    global main_hand
    elements = []
    for i in all_elements:
        elements.append(i)
    elements.remove(main_hand)
    
#Check if a matches have been found
def find_matches():
    global match_found
    while match_found==False:
        global matched_start_lines
        global latest_started_match
        global session_match
        global practice_match
        find_latest_log_file()
        #===============================================================================================================================#
        # Match start search  (Regular lobbies)      
        #===============================================================================================================================#
        matched_start_lines = search_string_in_file((latest_file), 'CONNECTING TO IP', 0)
        print("Looking for regular matches.")
        if  matched_start_lines:
            print ("Regular matches found. Filtering latest match.")
            latest_regular_match=matched_start_lines[(len(matched_start_lines)-1)]    
            #print ("latest: " +str(latest_regular_match))
            #print ("session: " +str(session_match))
            print("Checking if this is an old match.")
            #time.sleep(1)
            if str(latest_regular_match)==str(session_match):
                print("Old match, restarting function.")
                time.sleep(1)
                pass
            else:
                print("New regular match detected")
                latest_started_match=latest_regular_match
                session_match=(latest_started_match)
                # print(session_match)
                match_found==True
                #Not sure if return below is required. Further testing needed
                #return session_match
                return
        else: 
            print ("No regular matches found yet.")
            time.sleep(2) 
#===============================================================================================================================#
# Match start search  (Practice lobbies)      
#===============================================================================================================================#
        matched_start_lines = search_string_in_file((latest_file), 'LoadMap: /Game/Maps/Longshot/Practice', 0)
        print("Looking for practice matches.")
        if  matched_start_lines:
            print ("Practice matches found.Filtering latest match.")
            latest_practice_match=matched_start_lines[(len(matched_start_lines)-1)]
            #print ("latest: " +str(latest_practice_match))
            #print ("session: " +str(practice_match))
            print("Checking if this is an old match.")
            #time.sleep(1)
            if str(latest_practice_match)==str(practice_match):
                print("Old match, restarting function.")
                time.sleep(2)
                pass
            else:
                print("New practice match detected")
                latest_started_match=latest_practice_match
                practice_match=(latest_started_match)
                # print(session_match)
                match_found==True
                #Not sure if return below is required. Further testing needed
                #return session_match
                return
        else: 
            print ("No practice matches found yet.")
            time.sleep(3)     
       
#Assign the region/location of the screen that has to be looked over to find the off hand
def set_gauntlet_position():
    global region
    global gauntlet_swap
    with open(os.getenv('LOCALAPPDATA')+'\\g3\\Saved\\Config\\WindowsNoEditor\\GameUserSettings.ini', encoding="utf8") as f:
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
    global practice_match    
    global t1
    global t2
    global elements
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
    set_elements()
    set_gauntlet_position()
    set_special_keys()
    #Main hand found, setting rgb codes:
    Obs_hotkeys.set_elements()
    #Start checking for mouse input and start looking for end of match.
    t1 = Thread(target = find_completed_match)
    t2 = Thread(target = check_mouse_input)
    t1.start()
    t2.start()
    
def start():
    global session_match
    global start_complete_script
    global working_dir
    global practice_match
    working_dir=str(pathlib.Path(__file__).parent.absolute())
    session_match=()
    practice_match=()
    start_complete_script()
  
def reset_gauntlet_position():
    set_gauntlet_position()

root = Tk()
root.title("Gauntlet tracker")
root.geometry("250x250")

app = Frame(root)
app.grid()

start = Button(app, text="Start tracking", command=start)
reset_gauntlet_position = Button(app, text="Reset gauntlet position", command=reset_gauntlet_position)

start.grid()
reset_gauntlet_position.grid()
root.mainloop()