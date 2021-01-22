import yeelight
from yeelight import Bulb
from yeelight import LightType
def set_elements():
    global gauntlets
    bulb = Bulb("192.168.178.15")
    gauntlets = {
        'fire': lambda: print (bulb.set_rgb(255,0,0)),
        'toxic': lambda: print (bulb.set_rgb(0,255,0)),
        'ice': lambda: print (bulb.set_rgb(0,0,255)),
        'wind': lambda: print (bulb.set_rgb(255,255,0)),
        'lightning': lambda: print (bulb.set_rgb(127,0,255)),
        'stone': lambda: print (bulb.set_rgb(153,76,8)),
        'noodle': lambda: print (bulb.set_rgb(255,20,147)),
        'default': lambda: print (bulb.set_rgb(0,0,255))
    }





