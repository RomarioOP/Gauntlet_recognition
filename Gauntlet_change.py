#Manually testing gauntlet color sync when in practice lobbies since there are no log entries when you enter the practice lobby.
#To-do gauntlet swap region
#https://imgur.com/a/YClCDqN
#https://imgur.com/4s6WmvX
import win32api
import time
import pyautogui
import yeelight
from yeelight import Bulb
from yeelight import LightType
import glob
import os
main_hand="wind"

all_elements = ["wind", "toxic", "ice", "fire", "stone" ,"lightning", "noodle"]
elements = []
for i in all_elements:
    elements.append(i)
elements.remove(main_hand)

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

    time.sleep(0.5)



