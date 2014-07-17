import requests
import json
import uuid
import os.path

host = 'http://aws.onion.io/'
mfr = "ONION"
device_type="Computer"
firmware_version=""
hardware_version=""

functions={}
function_template=[]

def declare(function,endpoint,default={}):
    function_template.append({"function_id":endpoint,"params":default})
    functions[endpoint]=function
    return function_template

def register():
    conf_file='onion_dev'
    if not os.path.isfile(conf_file):
        addr = ''.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1]).upper()
        res=requests.get(host+"/ds/v1/register/{0}/{1}".format(mfr,addr)).json()
        if "error" in res:
            return res
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
    return devKey

def update_device():
    url=host+'ds/v1/declare/{0}'.format(devKey)
    data={"device_type":device_type,"firmware_version":firmware_version,"hardware_version":hardware_version,"functions":function_template}
    res=requests.post(url,data=json.dumps(data))
    return res

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

def loop():
    while True:
        try:
            for response in listen():
                if response["function_id"] != None: functions[response["function_id"]](response["params"])
        except requests.exceptions.Timeout: #survive timeouts
            pass