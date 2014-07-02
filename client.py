import requests
import json

host = 'http://aws.onion.io/'
functions={}

testKey = 'e5f0ff18-da97-4eac-8c18-104322373050' #some testing data
testId = '456789000'
devKey = testKey #these should read from non-volatile memory instead
devId = testId
mfr="ddTest" #this should be manufacturer specific
addr="123456789" #this should import the device MAC or generate a random address

def register():
    #replace defaults with correct values if device not yet registered
    res=json.load(requests.get(host+"/ds/register/{0}/{1}".format(mfr,addr)))
    if res["error"]: print res["error"]
    else:
        devId = res["deviceId"]
        devKey = res["deviceKey"]

def listen():
    url=host+'ds/v1/listen/{0}'.format(devKey)
    s=requests.Session()
    req=requests.Request("GET",url).prepare()
    res=s.send(req, stream=True, timeout=60)
    streambuffer = ''
    try: gen = res.iter_content()
    except httplib.IncompleteRead: pass
    for byte in gen:
        if byte:
            streambuffer += byte
            try:
                func = json.loads(streambuffer)
            except ValueError:
                continue
            yield func
            streambuffer = ''

def declare(function,endpoint):
    #check if on server, upload if not (server-side declaration not implmented yet)
    functions[endpoint]=function

def loop():
    while True:
        try:
            for response in listen():
                if response["function_id"] != None: functions[response["function_id"]](response["params"])
        except requests.exceptions.Timeout: #survive timeouts
            pass
