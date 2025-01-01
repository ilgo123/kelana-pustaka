from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    nik: str
    full_name: str
    birth_place: str
    birth_date: datetime
    gender: str
    address: str
    username: str
    email: str
    password: str
    role: str

    @classmethod
    def from_sheet_row(cls, row_data: dict):
        return cls(
            id=row_data.get('id'),
            nik=row_data.get('nik'),
            full_name=row_data.get('full_name'),
            birth_place=row_data.get('birth_place'),
            birth_date=row_data.get('birth_date'),
            gender=row_data.get('gender'),
            address=row_data.get('address'),
            username=row_data.get('username'),
            email=row_data.get('email'),
            password=row_data.get('password'),
            role=row_data.get('role'),
        )