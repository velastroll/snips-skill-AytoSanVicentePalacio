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

def intent_received(hermes, intentMessage):
    sentence = "Pues "
    for index, item in enumerate(intentMessage["slots"]):
        if item.rawValue == 'fax':
            sentence += "Encontrado Fax "
        if item.rawValue == 'email':
            sentence += " encontrado email "
        if item.rawValue == "telefono":
            sentence += " encontrado telefono "
    
    hermes.publish_end_session(intentMessage.session_id, sentence)
    
    
with Hermes(MQTT_ADDR) as h:
    h.subscribe_intents(intent_received).start()
