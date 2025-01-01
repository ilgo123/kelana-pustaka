from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Book:
    book_id: Optional[int]
    title: str
    isbn: str
    author: str
    available: bool
    synopsis: str
    publisher: str
    year_of_publication: int
    pages: int
    grants: bool
    borrower_now: Optional[str] = None
    borrow_date: Optional[datetime] = None
    borrow_due_date: Optional[datetime] = None
    count_borrow: Optional[int] = None
    stock: Optional[int] = None

    @classmethod
    def from_sheet_row(cls, row_data: dict):
        return cls(
            book_id=row_data.get('book_id'),
            title=row_data.get('title'),
            isbn=row_data.get('isbn'),
            author=row_data.get('writer'),
            synopsis=row_data.get('synopsis'),
            publisher=row_data.get('publisher'),
            year_of_publication=row_data.get('year_of_publication'),
            pages=row_data.get('pages'),
            grants=row_data.get('grants'),
            available=row_data.get('available') == 'TRUE',
            borrower_now=row_data.get('borrower_now'),
            borrow_date=datetime.fromisoformat(row_data['borrow_date']) if row_data.get('borrow_date') else None,
            borrow_due_date=datetime.fromisoformat(row_data['borrow_due_date']) if row_data.get('borrow_due_date') else None,
            count_borrow=row_data.get('count_borrow'),
            stock=row_data.get('stock'),
        )