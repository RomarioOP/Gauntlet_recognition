#Read usersettings to determine if gauntlet slots are swapped or not and set correct region for icon recognition
with open('C:\\Users\\romar\\AppData\\Local\\g3\\Saved\\Config\\WindowsNoEditor\\GameUserSettings.ini') as f:
    if 'bSwapGauntletSlots=False' in f.read():
        region=(660,900,600,100)
    else:
        region=("tbd")

print (region)