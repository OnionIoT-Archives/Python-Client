import client
import el_gpio
el_gpio.pinMode(19,'OUT')
state=0
def toggle_state(params):
    global state
    state=1-state
    el_gpio.digitalWrite(19,state)
client.declare(toggle_state,"testfunc")
