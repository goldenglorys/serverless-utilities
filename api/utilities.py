import os
import json
import gspread
from time import time
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date, datetime
from googleapiclient import discovery
import psycopg2
import psycopg2.extras

from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
CREDS_JSON_STR = os.getenv("CREDS_JSON_STR")

class Utilities:

    def __init__(self):
        self.users = self.get_all_users()

    def get_credentials(self):
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            json.loads(str(CREDS_JSON_STR)), scope
        )
        return credentials

    def get_sheet_meta_data(self, sheet_id):
        credentials = self.get_credentials()
        service = discovery.build('sheets', 'v4', credentials=credentials)
        spreadsheet_id = sheet_id
        request = service.spreadsheets().get(
            spreadsheetId=spreadsheet_id
        )
        response = request.execute()
        return response

    def get_drive(self):
        credentials = self.get_credentials()
        drive = discovery.build("drive", "v3", credentials=credentials)
        return drive

    def get_sheet(self, sheet_id, _range):
        credentials = self.get_credentials()
        service = discovery.build('sheets', 'v4', credentials=credentials)
        spreadsheet_id = sheet_id
        request = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, 
            range=_range,
        )
        response = request.execute()
        return response

    def get_sheet_with_formula(self, sheet_id, _range):
        credentials = self.get_credentials()
        service = discovery.build('sheets', 'v4', credentials=credentials)
        spreadsheet_id = sheet_id
        request = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, 
            range=_range,
            valueRenderOption="FORMULA"
        )
        response = request.execute()
        return response

    def update_sheet(self, sheet_id, _range, values):
        credentials = self.get_credentials()
        service = discovery.build('sheets', 'v4', credentials=credentials)
        request = service.spreadsheets().values().update(
            spreadsheetId=sheet_id, 
            range=_range, 
            valueInputOption='RAW', 
            body= {
                'values' : values,
                'majorDimension' : 'ROWS'
            }
        )
        response = request.execute()
        return response

    def get_db_conn(self):
        return psycopg2.connect(DATABASE_URL)

    def run_sql_query(self, sql):
        connection = self.get_db_conn()
        rows = []
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
        return [
            dict(row) for row in rows
        ]

    def run_simple_sql_query(self, sql):
        try:
            connection = self.get_db_conn()
            rows = []
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
            connection.commit()
            return [
                dict(row) for row in rows
            ]
        except:
            print(sql)
            return []

    def get_all_users(self):
        sql = """
            select id, name from credentials.users
        """
        return self.run_sql_query(sql)

    def find_user_id_by_name(self, name):
        match = [el for el in self.users if el["name"] == name]
        return match[0] if len(match)>0 else None

