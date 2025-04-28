from CiscoWheel.webex import Webex
from datetime import datetime, timedelta
from CiscoWheel.mongo_db import MongoDb
from base64 import b64encode
from base_alert import *
import re
class Deliver(BaseAlertCapture):
    def __init__(self):
        super().__init__()
        self.SCD_Alerts = "Y2lzY29zcGFyazovL3VzL1JPT00vMTBiY2Y4YjAtMmFkMy0xMWVlLWJlYWItYmJlZDNmNjI5Yjkw"
        self.room_ids.append({"name": "SCD - Alerts", "id": self.SCD_Alerts})
        self.asg = "deliver"
        last_update = self.mongo.get_last_update(self.asg, self.uctype).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self.get_inc_prb_alert_data(self.room_ids, last_update, self.parse_function)
        # Initialize additional attributes for Finance class here


    def parse_function(self, message):
        # Override the first method
        print("PARSE FUNCTION STARTED")
        if message["roomId"] == self.SCD_Alerts:
            # Parse the message and return title and summary
            try:
                if message.get("markdown"):
                    title = message["markdown"].split("\n")[0]
                    title = re.sub(r"[\*]*|&nbsp|;", '', title)  # Remove HTML tags
                if message.get("files"):
                    title = "Excel : " + message["text"].split("\n")[0]
                summary = message["text"]
                print("Message Parsed")
            except:
                print("Error Parsing Message")
                print(message)
                input("Press Enter to continue...")
            return title, summary


# Example usage
if __name__ == "__main__":
    obj = Deliver()
    # obj.method_one()
    # obj.method_two()