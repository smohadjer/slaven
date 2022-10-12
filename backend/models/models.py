from datetime import datetime


from pydantic import BaseModel, EmailStr, Field


class FormData(BaseModel):
    first_name: str = Field(..., description="First name of the person sending the form", example="John")
    last_name: str = Field(..., description="Last name of the person sending the form", example="Doe")
    address: str = Field(..., description="Adress of the person sending the form", example="Teststreet 21")
    city: str = Field(..., description="Name of the city where person lives", example="Freiburg")
    postal_code: str = Field(..., description="Postal code of the city where person lives", example="12354")
    birthday: datetime = Field(..., description="Birthday of the person sending the form", example="1990-01-01")
    phone: str = Field(..., description="Phone number of the person sending the form", example="+461234567")
    email: EmailStr = Field(..., description="Email of the person sending the form", example="johndoe@gmail.com")
    training_type: list[str] = Field(..., description="The type of trainings you could choose", example=["solo", "group"])
    training_time: list[str] = Field(..., description="The hours of trainings you could choose", example=["14-15", "15-16"])
    privacy: bool = Field(..., description="Allow privacy", example=True)
    year: int = Field(..., description="Year in regards to what year the event is taking place in", example=2023)
    season: str = Field(..., description="Season in regards to what season the event is taking place in", example="summer")


class FormEvent(FormData):
    timestamp: datetime = datetime.utcnow()

