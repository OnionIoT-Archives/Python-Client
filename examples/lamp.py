import client
import el_gpio

el_gpio.pinMode(16,'OUT')
el_gpio.digitalWrite(16,1)

def on(params):
    el_gpio.digitalWrite(16,0)
def off(params):
    el_gpio.digitalWrite(16,1)
client.declare(on,"on")
client.declare(off,"off")
