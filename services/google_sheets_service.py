from oauth2client.service_account import ServiceAccountCredentials
import gspread
import streamlit as st
from config import Config

class GoogleSheetsService:
    def __init__(self):
        self.book = self._authenticate_book()
        self.user = self._authenticate_user()

    def _authenticate_book(self):
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                Config.CREDENTIALS_FILE, 
                Config.SCOPES
            )
            client = gspread.authorize(creds)
            return client.open(Config.SHEET_NAME).worksheet(Config.BOOKSHEET_NAME)
        except Exception as e:
            st.error(f"Failed to connect to Google Sheets: {e}")
            return None
        
    def _authenticate_user(self):
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                Config.CREDENTIALS_FILE, 
                Config.SCOPES
            )
            client = gspread.authorize(creds)
            return client.open(Config.SHEET_NAME).worksheet(Config.USERSHEET_NAME)
        except Exception as e:
            st.error(f"Failed to connect to Google Sheets: {e}")
            return None

    def append_row(self, row_data):
        return self.book.append_row(row_data)

    def update_cells(self, cell_range, values):
        return self.book.update(cell_range, values)

    def find_cell(self, value):
        return self.book.find(value)

    def get_all_records(self):
        return self.book.get_all_records()
    
    def add_public_user(self, row_data):
        return self.user.append_row(row_data)
    
    def get_auth(self):
        return self.user.get_all_records() 
