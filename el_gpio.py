import time
def pinMode(num, mode):
    num=str(num).lower()
    mode=str(mode).lower()
    if mode=="input": mode="in"
    if mode=="output": mode="out"
    export=file("/sys/class/gpio/export","w")
    export.write(num)
    export.close()
    direction=file("/sys/class/gpio/gpio"+num+"/direction","w")
    direction.write(mode)
    direction.close()
def digitalWrite(num, write):
    num=str(num).lower()
    write=str(write).lower()
    if write=="high": write="1"
    if write=="low": write=="0"
    value=file("/sys/class/gpio/gpio"+num+"/value","w")
    value.write(write)
    value.close()
def digitalRead(num):
    num=str(num).lower()
    value=file("/sys/class/gpio/gpio"+num+"/value","r")
    read=value.readline()
    value.close()
    return int(read)
