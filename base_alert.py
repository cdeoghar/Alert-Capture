from CiscoWheel.webex import Webex
from CiscoWheel.mongo_db import MongoDb
from CiscoWheel.splunk_push import *
from base64 import b64encode
from random import choices
from datetime import datetime

class BaseAlertCapture:
    def __init__(self):
        # Initialize class attributes here
        self.webex = Webex()
        self.webex.headers["Authorization"] = "Bearer " + "YmUyODdmMjgtYjhhYi00ZWM0LWJlMDEtMWY3MzI4MDMwZDczMzU0OTZhNmQtYzk0_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
        print(self.webex.headers["Authorization"])
        self.mongo = MongoDb()
        self.uctype = "alert-capture"
        self.source_type = "alert_sample_1"
        self.room_ids = []

    def get_inc_prb_alert_data(self, room_ids, last_update, parse_function=None):
        time_now = datetime.now()
        now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        for room in room_ids:
            room_id = room["id"]
            data = self.get_webex_data(room_id, last_update, now)
            data_list = []
            i = 0
            for message in data["items"]:
                # aid = b64encode(f"{self.asg}_{message['created'].replace(':','').replace('-','').replace('Z','').replace('T', '')}_{time_now.timestamp()}_{i}".encode()).decode()
                i += 1
                t = {"criticality":choices([5,3], [9,1])[0], "alert_space": room["name"], "alert_id": message["id"], "track_name": self.asg, "source": "webex","alert_raw": message["text"][:1000], "alert_created_on": message["created"], "alert_sent_by": message["personEmail"]}
                t["alert_title"], t["alert_summary"] = parse_function(message)
                data_list.append(t)
                print(*t.items(), sep="\n", end="\n\n\n")
            print(data_list)

        push_bulk(data_list, self.uctype, self.asg, self.source_type)        
        self.mongo.update_last_update(self.asg, self.uctype, time_now)

    
    def get_webex_data(self, room_id, start_date, end_date):
        # Override the first method
        print("Finance get_webex_data called")
        return self.webex.get_message_list(room_id, start_date, end_date)
    
    def parse_function(self, message):
        # Override the second method
        print("PARSE FUNCTION NOT IMPLEMENTED")
        return None, None


    def get_email_data(self):
        # Define the second method
        pass