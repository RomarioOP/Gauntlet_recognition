import virtual_keystroke
def set_element_hotkeys():
    global gauntlets
    gauntlets = {
        'fire': lambda: virtual_keystroke.pressHoldRelease("alt", "1"),
        'toxic': lambda: virtual_keystroke.pressHoldRelease("alt", "2"),
        'ice': lambda: virtual_keystroke.pressHoldRelease("alt", "3"),
        'wind': lambda: virtual_keystroke.pressHoldRelease("alt", "4"),
        'lightning': lambda: virtual_keystroke.pressHoldRelease("alt", "5"),
        'stone': lambda: virtual_keystroke.pressHoldRelease("alt", "6"),
        'noodle': lambda: virtual_keystroke.pressHoldRelease("alt", "7")
    }
