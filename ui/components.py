import streamlit as st
from datetime import datetime

class UIComponents:
    @staticmethod
    def render_book_table(books: list, include_borrower: bool = False):
        if not books:
            st.info("No books available")
            return

        data = [{
            "ID": book.book_id,
            "Judul": book.title,
            "Penulis": book.author,
            "ISBN": book.isbn,
            "Sinopsis": book.synopsis,
            "Penerbit": book.publisher,
            "Tahun Terbit": book.year_of_publication,
            "Hal": book.pages,
            "Hibah": "✔" if book.grants == "TRUE" else "❌",
            **({"Borrower": book.borrower_now,
                "Borrow Date": book.borrow_date.strftime("%Y-%m-%d") if book.borrow_date else "",
                "Due Date": book.borrow_due_date.strftime("%Y-%m-%d") if book.borrow_due_date else ""
               } if include_borrower else {})
        } for book in books]
        
        st.dataframe(data, use_container_width=True)