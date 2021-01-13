#Main script 
import win32api
import time
import pyautogui
import yeelight
from yeelight import Bulb
from yeelight import LightType
import glob
import os


#https://thispointer.com/python-search-strings-in-a-file-and-get-line-numbers-of-lines-containing-the-string/
#https://stackoverflow.com/questions/39327032/how-to-get-the-latest-file-in-a-folder


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


#print('Total Matched lines : ', len(matched_lines))

lastest_match=matched_lines[(len(matched_lines)-1)]



for elem in lastest_match:
    #print('Line Number = ', elem[0], ' :: Line = ', elem[1])
    if "Pyromancer" in str(lastest_match):
        main_hand="fire"
    elif "Tempest" in str(lastest_match):
        main_hand="wind"
    elif "Conduit" in str(lastest_match):
        main_hand="lightning"
    elif "Stonehaper" in str(lastest_match):
        main_hand="stone"
    elif "Toxicologist" in str(lastest_match):
        main_hand="toxic"
    elif "Frostborn" in str(lastest_match):
        main_hand="ice"
print (main_hand)

#assign the light
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

elements = []
for i in all_elements:
    elements.append(i)
elements.remove(main_hand)


with open('C:\\Users\\romar\\AppData\\Local\\g3\\Saved\\Config\\WindowsNoEditor\\GameUserSettings.ini') as f:
    if 'bSwapGauntletSlots=False' in f.read():
        region=(660,900,600,100)
    else:
        region=("tbd")


global last_used_gauntlet
last_used_gauntlet=""
last_offhand=""
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


special_keys = [0x01, 0x02]
special = {0x01: 'leftClick',
           0x02: 'rightClick',}
time.sleep(1)

while True: 
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