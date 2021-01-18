#Manually setting yeelight color for testing purposes.
import yeelight
from yeelight import Bulb
from yeelight import LightType

bulb = Bulb("192.168.178.15")
rgb = {
	'fire': lambda: print (bulb.set_rgb(255,0,0)),
	'toxic': lambda: print (bulb.set_rgb(0,255,0)),
	'ice': lambda: print (bulb.set_rgb(0,0,255)),
	'wind': lambda: print (bulb.set_rgb(255,255,0)),
	'lightning': lambda: print (bulb.set_rgb(51,0,102)),
	'stone': lambda: print (bulb.set_rgb(255,126,0)),
    'noodle': lambda: print (bulb.set_rgb(255,239,213))
}

rgb['toxic']()