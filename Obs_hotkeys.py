import virtual_keystroke
def set_elements():
    global gauntlets
    gauntlets = {
        'fire': lambda: virtual_keystroke.pressHoldRelease("F1"),
        'toxic': lambda: virtual_keystroke.pressHoldRelease("F2"),
        'ice': lambda: virtual_keystroke.pressHoldRelease("F3"),
        'wind': lambda: virtual_keystroke.pressHoldRelease("F4"),
        'lightning': lambda: virtual_keystroke.pressHoldRelease("F5"),
        'stone': lambda: virtual_keystroke.pressHoldRelease("F6"),
        'noodle': lambda: virtual_keystroke.pressHoldRelease("F7"),
        'default': lambda: virtual_keystroke.pressHoldRelease("F8")
    }
