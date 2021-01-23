import virtual_keystroke
def set_elements():
    global gauntlets
    gauntlets = {
        'dragonfire': lambda: virtual_keystroke.pressHoldRelease("F1"),
        'todoroki': lambda: virtual_keystroke.pressHoldRelease("F2"),
        'fire whirl': lambda: virtual_keystroke.pressHoldRelease("F3"),
        'plasma': lambda: virtual_keystroke.pressHoldRelease("F4"),
        'lava': lambda: virtual_keystroke.pressHoldRelease("F5"),
        'contamination': lambda: virtual_keystroke.pressHoldRelease("F6"),
        'mad scientist': lambda: virtual_keystroke.pressHoldRelease("F7"),
        'blizzard': lambda: virtual_keystroke.pressHoldRelease("F8"),
        'arctic lightning': lambda: virtual_keystroke.pressHoldRelease("F9"),
        'glacier': lambda: virtual_keystroke.pressHoldRelease("F10"),
        'storm': lambda: virtual_keystroke.pressHoldRelease("F11")
    }
