import streamlit as st

class Config:
    SHEET_NAME = 'DBKelanaPustaka'
    BOOKSHEET_NAME = 'Book'
    USERSHEET_NAME = 'User'
    SCOPES = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]