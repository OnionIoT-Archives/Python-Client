import requests
import json
import uuid
import os.path

mfr="ONION"

host = 'http://aws.onion.io/'
functions={}

def register():
    conf_file='onion_dev'
    if not os.path.isfile(conf_file):
        addr = ''.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1]).upper()
        res=requests.get(host+"/ds/v1/register/{0}/{1}".format(mfr,addr)).json()
        if "error" in res:
            print res["error"]
            return
        config = open(conf_file,'w')
        config.write(str(res["deviceId"])+'\n')
        config.write(str(res["deviceKey"])+'\n')
	    config.close()
    config=open(conf_file,'r')
    global devId
    devId = config.readline().rstrip()
    global devKey
    devKey = config.readline().rstrip()
    config.close()
    return

def listen():
    url=host+'ds/v1/listen/{0}'.format(devKey)
    s=requests.Session()
    req=requests.Request("GET",url).prepare()
    res=s.send(req, stream=True, timeout=60)
    streambuffer = ''
    gen = res.iter_content()
    try:
        for byte in gen:
            if byte:
                streambuffer += byte
                try:
                    func = json.loads(streambuffer)
                except ValueError:
                    continue
                yield func
                streambuffer = ''
    except requests.exceptions.ChunkedEncodingError: pass

def declare(function,endpoint):
    #check if on server, upload if not (server-side declaration not implemented yet)
    functions[endpoint]=function

def loop():
    while True:
        try:
            for response in listen():
                if response["function_id"] != None: functions[response["function_id"]](response["params"])
        except requests.exceptions.Timeout: #survive timeouts
            pass

register()