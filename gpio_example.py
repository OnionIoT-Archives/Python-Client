import el_gpio
pinMode(19,'out')
pinMode(20,'in')
state = 0
while(True):
    mode=digitalRead(20)
    if mode == 1: speed = 1
    else: speed = .1
    digitalWrite(19,state)
    state = 1 - state
    time.sleep(speed)
