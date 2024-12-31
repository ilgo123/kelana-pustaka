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
    available: bool
    gender: str
    address: str
    username: str
    email: str
    password: str
    role: str