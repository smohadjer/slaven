from pydantic import BaseModel, EmailStr


class FormData(BaseModel):
    firstname: str
    lastname: str
    address: str
    city: str
    postalcode: str
    birthday: str
    phone: str
    email: EmailStr
    training_type: list[str]
    training_time: list[str]
    privacy: str

