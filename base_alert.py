from CiscoWheel.webex import Webex
from CiscoWheel.mongo_db import MongoDb
from CiscoWheel.splunk_push import *
from CiscoWheel.email_alert import get_outlook_data
from base64 import b64encode
from random import choices
from datetime import datetime, timedelta
from generate_token import read_token_from_file, get_tokens_refresh_static

class BaseAlertCapture:
    mongo = MongoDb()
    mail_list = get_outlook_data("Alert Capture", mongo.get_last_update("mix", "Alert-Capture-Email"), datetime.now())
    mongo.update_last_update("mix", "Alert-Capture-Email", datetime.now()-timedelta(days=1))
    webex = Webex()

    def __init__(self):
        # input(self.mail_list)
        # Initialize class attributes here
        self.webex.headers["Authorization"] = None
        self.reset_token()
        print(self.webex.headers["Authorization"])
        self.uctype = "alert-capture"
        self.source_type = "alert_sample_1"
        self.room_ids = []

    def reset_token(self, flag=False):
        if flag:
            access_token, refresh_token = get_tokens_refresh_static(read_token_from_file("refresh_token"))
            self.webex.headers["Authorization"] = "Bearer " + access_token
            return access_token

        access_token = "Bearer " + str(read_token_from_file("access_token"))
        self.webex.headers["Authorization"] =  "Bearer " + access_token
        return access_token

    def get_inc_prb_alert_data(self, room_ids, last_update, parse_function=None):
        time_now = datetime.now()
        now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        data_list = []
        for room in room_ids:
            # input(f"{room['name']}: PRESS ENTER TO CONTINUE")
            room_id = room["id"]
            data = self.get_webex_data(room_id, last_update, now)
            i = 0
            for message in data["items"]:
                # aid = b64encode(f"{self.asg}_{message['created'].replace(':','').replace('-','').replace('Z','').replace('T', '')}_{time_now.timestamp()}_{i}".encode()).decode()
                i += 1
                t = {"criticality": None, "alert_space": room["name"], "alert_id": message["id"], "track_name": self.asg, "alert_source": "webex","alert_raw": message["text"][:1000], "alert_created_on": message["created"], "alert_sent_by": message["personEmail"]}
                t.update(parse_function(message))
                data_list.append(t)
                print(*t.items(), sep="\n", end="\n\n\n")
            # print(data_list)
        data_list.extend(self.get_email_data())

        push_bulk(data_list, self.uctype, self.asg, self.source_type)        
        self.mongo.update_last_update(self.asg, self.uctype, time_now)

    
    def get_webex_data(self, room_id, start_date, end_date):
        # Override the first method
        print("Finance get_webex_data called")
        res = self.webex.get_message_list(room_id, start_date, end_date)
        if type(res) == str and res.startswith("NO DATA RETRIEVED"):
            self.reset_token(True)
            res = self.webex.get_message_list(room_id, start_date, end_date)
        return res
    
    def parse_function(self, message):
        # Override the second method
        print("PARSE FUNCTION NOT IMPLEMENTED")
        return None, None


    def get_email_data(self, track):
        # Define the second method
        pass