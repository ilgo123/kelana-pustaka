from oauth2client.service_account import ServiceAccountCredentials
import gspread
import streamlit as st
from config import Config

class GoogleSheetsService:
    credentials = {
            "type": st.secrets["type"],
            "project_id": st.secrets["project_id"],
            "private_key_id": st.secrets["private_key_id"],
            "private_key": st.secrets["private_key"],
            "client_email": st.secrets["client_email"],
            "client_id": st.secrets["client_id"],
            "auth_uri": st.secrets["auth_uri"],
            "token_uri": st.secrets["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["client_x509_cert_url"]
        }

    def __init__(self):
        self.book = self._authenticate_book()
        self.user = self._authenticate_user()

    def _authenticate_book(self):
        try:
            # creds = ServiceAccountCredentials.from_json_keyfile_name(
            #     Config.CREDENTIALS_FILE, 
            #     Config.SCOPES
            # )
            client = gspread.service_account_from_dict(self.credentials)
            return client.open(Config.SHEET_NAME).worksheet(Config.BOOKSHEET_NAME)
        except Exception as e:
            st.error(f"Failed to connect to Google Sheets: {e}")
            return None
        
    def _authenticate_user(self):
        try:
            # creds = ServiceAccountCredentials.from_json_keyfile_name(
            #     Config.CREDENTIALS_FILE, 
            #     Config.SCOPES
            # )
            client = gspread.service_account_from_dict(self.credentials)
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
