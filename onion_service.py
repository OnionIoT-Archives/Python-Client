import time
import logging
import urllib
import sys
import json

LOG_FILENAME = 'default_log.out'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logging.info(time.ctime()+': Client Started')

from default_script import *

def update(params):
    urllib.urlretrieve(params["url"],"default_script.py")
    sys.exit()
client.declare(update,"update",{"url":""})

status=client.register()
logging.info("Registered at "+status)
status=client.update_device()
logging.info("Updated: "+status.content)

try:
    client.loop()
except:
    logging.exception('Client Loop failed!')
