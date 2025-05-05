from CiscoWheel.webex import Webex
from datetime import datetime, timedelta
from CiscoWheel.mongo_db import MongoDb
from base64 import b64encode
from base_alert import *

alert_criticality_mapping = {
    "Cisco Costing DCR Main Wrapper program | q7 : query | state : Validation Failed": "P1",
    "PCAM Data Receival query | q17 : query | state : Initiated": "P5",
    "Cisco X1 Writeback program | q3 : query | state : Initiated": "P1",
    "DCR program | q7.1 : query | state : Validated": "P1",
    "Excel : Hybrid Order Query | q9 : query | state : Executed": "P5",
    "XLA to GL stuck query | q11 : query | state : Initiated": "P1",
    "Lease Classification query | q12 : query | state : Initiated": "P5",
    "Cisco Costing DCR Main Wrapper program | q7 : query | state : Initiated": "P1",
    "Hybrid Order Query | q9 : query | state : Initiated": "P5",
    "Excel : XLA to GL stuck query | q11 : query | state : Executed": "P1",
    "Excel : Lease Classification query | q12 : query | state : Validated": "P5",
    "RTV Failures query | q14 : query | state : Initiated": "P1",
    "Anthena/omega orders query | q10 : query | state : Initiated": "P5",
    "Cisco X1 Writeback program | q3 : query | state : Validated": "P1",
    "COGS Eligible records query | q16 : query | state : Initiated": "P5",
    "Cisco Costing Meraki Costing Program | q1 : query | state : Initiated": "Disabled",
    "Meraki Item Cost Receival | q2 : query | state : Validated": "P5",
    "DCR program | q7.1 : query | state : Initiated": "P1",
    "X1 Writeback Check query | q3.1 : query | state : Initiated": "P1",
    "Excel : COGS Eligible records query | q16 : query | state : Executed": "P5",
    "Excel : Anthena/omega orders query | q10 : query | state : Executed": "P5",
    "Meraki Item Cost Receival | q2 : query | state : Initiated": "P5"
}

class Finance(BaseAlertCapture):
    def __init__(self):
        super().__init__()
        self.CRITICAL_TRANSACTION_JOBS_ALERT = "Y2lzY29zcGFyazovL3VzL1JPT00vMWRhZDYyNDAtZTkxMi0xMWVmLWIwOTgtMjc2Y2FkMGQ5NGIw"
        self.room_ids.append({"name": "Critical Transaction Jobs Alert", "id": self.CRITICAL_TRANSACTION_JOBS_ALERT})
        self.asg = "Finance"
        last_update = self.mongo.get_last_update(self.asg, self.uctype).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self.get_inc_prb_alert_data(self.room_ids, last_update, self.parse_function)
        # Initialize additional attributes for Finance class here

    def get_criticality(self, message):
        for i in alert_criticality_mapping:
            if message[:30] in i or i in message:
                return alert_criticality_mapping[i]
        return None 
    
    def get_alert_type(self, message):
        return "Transaction Monitoring"

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
            crit = self.get_criticality(title)
            return {"alert_title": title, "alert_summary": summary, "criticality": crit, "alert_type": self.get_alert_type(title)}


    def get_email_data(self):
        # Override the second method
        data_list = []
        for i in self.mail_list:
            if "Finance" in i["body"]:
                print(f"{i['subject']} : {i['sender']} : {i['received_time']}")
                
                t = {
                    "criticality": self.get_criticality(i['body']),
                    "alert_id": b64encode(f"{self.asg}{i['received_time']}{i['sender']}".encode()).decode(), 
                    "track_name": self.asg, 
                    "alert_source": "email",
                    "alert_raw": i['body'],
                    "alert_title": i['subject'],
                    "alert_summary": i['body'],
                    "alert_created_on": i['received_time'], 
                    "alert_sent_by": i['sender'],
                }
                print(*t.items(), sep="\n", end="\n\n\n")
                # input("Press Enter to continue...")
                data_list.append(t)
        print("EMAIL DATA LIST :", data_list)
        return data_list

# Example usage
if __name__ == "__main__":
    obj = Finance()
    # obj.method_one()
    # obj.method_two()