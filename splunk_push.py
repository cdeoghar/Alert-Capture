from CiscoWheel.mongo_db import MongoDb
from datetime import datetime
import pytz
import requests
import json


COLLECTOR_URL = "https://sra-lb-dmz-rcdn.cisco.com/services/collector"
SPLUNK_HEADER = {'Authorization': 'Splunk fa7fc89e-beac-4c9e-9633-31f38ab27641'}

DEV_COLLECTOR_URL = "https://sra-lb-dmz-nprd.cisco.com/services/collector"
DEV_SPLUNK_HEADER = {'Authorization': 'Splunk 0e87d487-969e-4fbf-aba9-bc9e7adfe4bf'}

def set_credentials(env):
    global COLLECTOR_URL, SPLUNK_HEADER
    if env == 'dev':
        COLLECTOR_URL = DEV_COLLECTOR_URL
        SPLUNK_HEADER = DEV_SPLUNK_HEADER
    else:
        raise ValueError("Invalid environment. Use 'dev' to set development credentials.")

MAX_BUFFER = 1000


mongo = MongoDb()
pacific_timezone = pytz.timezone('America/Los_Angeles')

def process_data(i, sourcetype):
    for k, v in i.items():
        if isinstance(v, datetime):
            pacific_time = v.astimezone(pacific_timezone)
            i[k] = pacific_time.strftime('%Y-%m-%d %H:%M:%S')
        if v != v:
            print(k, v)
            i[k] = None
    t = {"sourcetype": sourcetype}
    t["event"] = i
    t["fields"] = i
    return t

def push_bulk(res, uctype, asg, sourcetype):
    last_update = mongo.get_last_update(asg, uctype)
    for j in range(0, len(res), MAX_BUFFER):
        result = res[j:j + MAX_BUFFER]
        data_list = []
        for i in result:
            t = process_data(i, sourcetype)
            data_list.append(t)

    response = requests.post(COLLECTOR_URL, headers=SPLUNK_HEADER, json=data_list)
    print("SPLUNK RESPONSE:" , response, response.json())