from datetime import datetime, timedelta, date
from models.book import Book
from models.user import User
from services.google_sheets_service import GoogleSheetsService
import streamlit as st

class LibraryService:
    def __init__(self):
        self.sheets_service = GoogleSheetsService()

    def add_book(self, title: str, author: str, isbn: str) -> Book:
        new_data = [None, title, isbn, author, True]
        try:
            self.sheets_service.append_row(new_data)
            return Book(None, title, isbn, author, True)
        except Exception as e:
            raise Exception(f"Failed to add book: {e}")
        
    def grant_book(self, title: str, author: str, isbn: str) -> Book:
        new_data = [None, title, isbn, author, True, 
                    None, None, None, None, None, 
                    None, None, None, True]
        try:
            self.sheets_service.append_row(new_data)
            return Book(None, title, isbn, author, True)
        except Exception as e:
            raise Exception(f"Failed to grant book: {e}")

    def borrow_book(self, book_title: str, student_name: str) -> bool:
        available_books = self.get_available_books()
        book = next((b for b in available_books if b.title == book_title), None)
        
        if book:
            updated_data = [
                False, 
                student_name, 
                datetime.now().isoformat(), 
                (datetime.now() + timedelta(days=14)).isoformat()
            ]
            cell = self.sheets_service.find_cell(book.isbn)
            self.sheets_service.update_cells(
                f'E{cell.row}:H{cell.row}', 
                [updated_data]
            )
            return True
        return False

    def return_book(self, book_id: int) -> bool:
        borrowed_books = self.get_borrowed_books()
        book = next((b for b in borrowed_books if b.id == book_id), None)
        
        if book:
            cell = self.sheets_service.find_cell(book.isbn)
            self.sheets_service.update_cells(
                f'E{cell.row}:H{cell.row}', 
                [[True, "", "", ""]]
            )
            return True
        return False

    def get_available_books(self) -> list[Book]:
        records = self.sheets_service.get_all_records()
        return [Book.from_sheet_row(record) 
                for record in records 
                if record['available'] == 'TRUE']

    def get_borrowed_books(self) -> list[Book]:
        records = self.sheets_service.get_all_records()
        return [Book.from_sheet_row(record) 
                for record in records 
                if record['available'] == 'FALSE']
    
    def add_user_public(self, nik: str, full_name: str, birth_place: str, birth_date: date, gender: str, address: str, username: str, email: str, password: str) -> User:
        new_data = [None, nik, full_name, birth_place, birth_date.strftime("%Y-%m-%d"), gender, address, username, email, password, "customer"]
        try:
            self.sheets_service.add_public_user(new_data)
            return User(None, nik, full_name, birth_place, birth_date, gender, address, username, email, password, "customer")
        except Exception as e:
            raise Exception(f"Failed to add user: {e}")
        
    def auth(self, username: str, password: str) -> bool:
        try:
            result = self.sheets_service.get_auth()
            # Check if the username and password match any record
            user_found = False
            for user in result:
                if user['username'] == username and user['password'] == password:
                    user_found = True
                    st.session_state.role = user['role'] 
                    break

            if user_found:
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"Failed to authenticate: {e}")
        
        