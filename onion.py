import mosquitto
import json

isRuning = False
mqtt = mosquitto.Mosquitto()
callbacks=[None]
_deviceId=''

def onMessage(mosq, obj, msg):
    try:
        data = msg.payload.split(';')
        functionId = int(data[0])
        params = None
        if len(data)>1:
            params = data[1].split(',')
        callbacks[functionId](params)
    except Exception as e:
        print "Error: "+str(e)

def start():
    mqtt.loop_forever()
   # while isRuning:
   #     result = mqtt.loop()
   #     if result!=0:
   #         print result
   #         #mqtt.reconnect()


def init(deviceId, passwd):
    global _deviceId
    _deviceId = deviceId
    mqtt.username_pw_set(deviceId, passwd);
    mqtt.connect("mqtt.onion.io", port=1883, keepalive=60)
    mqtt.publish("/register", "%s;CONNECTED"%deviceId)
    mqtt.subscribe('/'+deviceId, 0)
    mqtt.on_message = onMessage

    global isRuning
    isRuning = True

def stop():
    global isRuning
    isRuning = False
    mqtt.disconnect()


def get(path, callback):
    functionId = len(callbacks)
    callbacks.append(callback)
    mqtt.publish("/register", "%s;GET;%s;%s"%(_deviceId, path, functionId))

def post(path, callback, params):
    functionId = len(callbacks)
    callbacks.append(callback)
    mqtt.publish("/register", "%s;POST;%s;%s;%s"%(_deviceId, path, functionId,params))

def update(path, value):
    mqtt.publish("/register", "%s;UPDATE;%s;%s"%(_deviceId, path, value))







