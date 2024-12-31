import streamlit as st

class Config:
    SHEET_NAME = 'DBKelanaPustaka'
    BOOKSHEET_NAME = 'Book'
    USERSHEET_NAME = 'User'
    CREDENTIALS_FILE = 'kelana-pustaka-124a8ed29086.json'
    SCOPES = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]