from CiscoWheel.webex import Webex
from datetime import datetime, timedelta
from CiscoWheel.mongo_db import MongoDb
from base64 import b64encode
from base_alert import *
import re


alert_data = {
    "TTM COB Planning Partial": "Order Processing Alerts",
    "Shipconfirm not processed": "Order Processing Alerts",
    "TTM CRT planning failed": "Order Processing Alerts",
    "Delivery Creation Issues(Order Change/LPN Not Packed)": "Order Processing Alerts",
    "TTM - Incoterm not generated": "Order Processing Alerts",
    "TTM - Multiple Outbound in TT Log": "Order Processing Alerts",
    "TTM Milestone template not assigned": "Order Processing Alerts",
    "ATTR Hold Count": "Order Processing Alerts",
    "Control-M Jobs Running more than half an hour": "Control-M Alerts",
    "TTM SLO trx - Outbound not sent": "Order Processing Alerts",
    "Concurrent Progam Running more than an hour": "Concurrent Progam Alerts",
    "TTM Inbound Events Processing": "Order Processing Alerts",
    "TTM MFG - No Outbound in TT Log": "Order Processing Alerts",
    "3B3 Backlog": "Order Processing Alerts",
    "3B2RTV in I_ERROR": "Order Processing Alerts",
    "4B2 stuck in DELIVERY_ERROR due to Order Change": "Order Processing Alerts",
    "TTM Inbound Transmission not Processed": "Order Processing Alerts",
    "Control-M Jobs Failure": "Control-M Alerts",
    "Route Code Issues - XXGCO vs RIQHDR": "Order Processing Alerts",
    "3B18 not transmitted to partners": "Order Processing Alerts",
    "Docs not interfaced to GTM-D": "Order Processing Alerts",
    "Concurrent Progam having multiple schedules": "Concurrent Progam Alerts",
    "TTM SLO/OPL Screening party errors": "Order Processing Alerts",
    "TTM - Other GTM trx timeout errors": "Order Processing Alerts",
    "Orders Awaiting Export Info from GTM": "Order Processing Alerts",
    "TTM CRT Location Profile Missing": "Order Processing Alerts",
    "RS_SCD_Long_Running_CNTRLM_Job_ALERT": "Control-M Alerts",
    "RS_SCD_CNTRLM_FAILURE_ALERT": "Control-M Alerts",
    "TTM - GTM SLO_OPL timeout errors": "Order Processing Alerts",
}


class Deliver(BaseAlertCapture):
    def __init__(self):
        super().__init__()
        self.SCD_Alerts = "Y2lzY29zcGFyazovL3VzL1JPT00vMTBiY2Y4YjAtMmFkMy0xMWVlLWJlYWItYmJlZDNmNjI5Yjkw"
        self.SCD_Atachments = "Y2lzY29zcGFyazovL3VzL1JPT00vOTczZDA5ZjAtZTVlNy0xMWVlLWFlMTQtODNjMzE3NmRkMDRi"
        self.SCD_ControlM_Alerts = "Y2lzY29zcGFyazovL3VzL1JPT00vOTdhOWRlNTAtNjFlMi0xMWVmLWIyNzAtMWJkZDc4NmU2NGRl"
        self.room_ids.extend([{"name": "SCD - Alerts", "id": self.SCD_Alerts}, {"name": "SCD - Attachments", "id": self.SCD_Atachments}, {"name": "SCD - ControlM Alerts", "id": self.SCD_ControlM_Alerts}])
        self.asg = "Deliver"
        last_update = self.mongo.get_last_update(self.asg, self.uctype).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self.get_inc_prb_alert_data(self.room_ids, last_update, self.parse_function)
        # Initialize additional attributes for Finance class here

    def get_alert_type(self, message):
        for i in alert_data:
            # print(i, message[:-6])
            if i in message:
                return alert_data[i]
        return None
    
    def parse_function(self, message):
        # Override the first method
        print("PARSE FUNCTION STARTED")
        if message["roomId"] in [self.SCD_Alerts, self.SCD_Atachments, self.SCD_ControlM_Alerts]:
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
            crit = "P5"
            return {"alert_title": title, "alert_summary": summary, "criticality": crit, "alert_type": self.get_alert_type(title)}


# Example usage
if __name__ == "__main__":
    obj = Deliver()
    # obj.method_one()
    # obj.method_two()