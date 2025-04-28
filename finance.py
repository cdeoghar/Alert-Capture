from CiscoWheel.webex import Webex
from datetime import datetime, timedelta
from CiscoWheel.mongo_db import MongoDb
from base64 import b64encode
from base_alert import *

class Finance(BaseAlertCapture):
    def __init__(self):
        super().__init__()
        self.CRITICAL_TRANSACTION_JOBS_ALERT = "Y2lzY29zcGFyazovL3VzL1JPT00vMWRhZDYyNDAtZTkxMi0xMWVmLWIwOTgtMjc2Y2FkMGQ5NGIw"
        self.room_ids.append({"name": "Critical Transaction Jobs Alert", "id": self.CRITICAL_TRANSACTION_JOBS_ALERT})
        self.asg = "Finance"
        last_update = self.mongo.get_last_update(self.asg, self.uctype).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self.get_inc_prb_alert_data(self.room_ids, last_update, self.parse_function)
        # Initialize additional attributes for Finance class here

    def parse_function(self, message):
        # Override the first method
        if message["roomId"] == self.CRITICAL_TRANSACTION_JOBS_ALERT:
            # Parse the message and return title and summary
            try:
                if message.get("html"):
                    title = message["html"].split("\n")[0]
                if message.get("files"):
                    title = "Excel : " + message["text"].split("\n")[0]
                summary = message["text"]
                print("Message Parsed")
            except:
                print("Error Parsing Message")
                print(message)
                input("Press Enter to continue...")
            return title, summary


    def method_two(self):
        # Override the second method
        print("Finance method_two called")

# Example usage
if __name__ == "__main__":
    obj = Finance()
    # obj.method_one()
    # obj.method_two()