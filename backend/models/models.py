from datetime import datetime


from pydantic import BaseModel, EmailStr


class FormData(BaseModel):
    first_name: str
    last_name: str
    address: str
    city: str
    postal_code: str
    birthday: datetime
    phone: str
    email: EmailStr
    training_type: list[str]
    training_time: list[str]
    privacy: bool
    year: int
    season: str


class FormEvent(FormData):
    timestamp: datetime = datetime.utcnow()

