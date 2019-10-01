#!/usr/bin/env python3
from hermes_python.hermes import Hermes
import hermes_python 
from urls_ayto import urls_dict
import json

cache_file = "cache.json"   # sets the name of the cache file

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883 
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT)) 


# open the cache file and read the json
with open (cache_file, "r") as read_file:
    cache = json.load(read_file)

f = open("/home/pi/exportation.json", "w+")

print(">>>", cache)
print("telefono: ", cache["telephone"])

# https://docs.snips.ai/reference/dialogue#intent-classification
def intent_received(hermes, intentMessage):
    sentence = "Pues "
    if intentMessage.slots[0].value == 'fax':
        sentence += "Encontrado Fax "
    if intentMessage.slots[0].value == 'email':
        sentence += " encontrado email "
    if intentMessage.slots[0].value == "telefono":
        sentence += " encontrado telefono "

    
    hermes.publish_end_session(intentMessage.session_id, sentence)
    
    
with Hermes(MQTT_ADDR) as h:
    h.subscribe_intents(intent_received).start()
