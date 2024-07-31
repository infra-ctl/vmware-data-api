import gspread
from colour import Color
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import logging
import random
import string


class GoogleSheetManager:
    def __init__(self, creds_file, sheet_id, sheet_name):
        self.scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        try:
            self.creds = Credentials.from_service_account_file(creds_file, scopes=self.scopes)
            self.client = gspread.authorize(self.creds)
            self.service = build("sheets", "v4", credentials=self.creds)
            self.sheet = self.service.spreadsheets()
            self.sheet_id = sheet_id
            self.sheet_name = sheet_name
        except Exception as e:
            logging.exception("Failed to initialize GoogleSheetManager")
            raise

    def clear_sheet(self):
        range_all = f"{self.sheet_name}!A:Z"

        try:
            self.sheet.values().clear(spreadsheetId=self.sheet_id, body={}, range=range_all).execute()
        except Exception as e:
            logging.exception("Failed to clear sheet")
            raise

    def titles(self, titles):
        self.length = len(titles)
        range = f'{self.sheet_name}!A1:{string.ascii_uppercase[self.length]}'
        
        try:
            body = {"values": [titles]}
            self.sheet.values().append(
                spreadsheetId=self.sheet_id, range=range, valueInputOption="RAW", body=body
            ).execute()

            requests = [
                {
                    "repeatCell": {
                        "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": len(titles)},
                        "cell": {"userEnteredFormat": {"textFormat": {"bold": True}}},
                        "fields": "userEnteredFormat.textFormat.bold"
                    }
                },
                {
                    "repeatCell": {
                        "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": len(titles)},
                        "cell": {"userEnteredFormat": {"backgroundColor": {"red": random.uniform(0.8, 0.1), "green": random.uniform(0.8, 0.1), "blue": random.uniform(0.8, 0.1)}}},
                        "fields": "userEnteredFormat.backgroundColor" 
                    }
                }
            ]

            self.sheet.batchUpdate(spreadsheetId=self.sheet_id, body={"requests": requests}).execute()
        except Exception as e:
            logging.exception("Failed to write titles to sheet")
            raise

    def append_data(self, data):
        range = f"{self.sheet_name}!A2:{string.ascii_uppercase[self.length]}"

        try:
            body = {"values": [data]}
            self.sheet.values().append(
                spreadsheetId=self.sheet_id, range=range, valueInputOption="RAW", body=body
            ).execute()

        except Exception as e:
            logging.exception("Failed to append data to sheet")


    def colour_data(self, hosts, colors=None):
        index = 1
        endindex = 1

        for host in hosts.values():
            endindex += host
            colour = (0,)
            
            while sum(colour) < 1.5:
                colour = (random.random(), random.random(), random.random())

            requests = [
                {
                    "repeatCell": {
                        "range": {"sheetId": 0, "startRowIndex": index, "endRowIndex": endindex, "startColumnIndex": 0, "endColumnIndex": self.length},
                        "cell": {"userEnteredFormat": {"backgroundColor": {"red": colour[0], "green": colour[1], "blue": colour[2]}}},
                        "fields": "userEnteredFormat.backgroundColor"
                    }
                }
            ]

            self.sheet.batchUpdate(spreadsheetId=self.sheet_id, body={"requests": requests}).execute()
            
            index = endindex
            