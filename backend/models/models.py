from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class AgeGroup(str, Enum):
    JUGEND = "jugend"
    ERWACHSENE = 'erwachsene'


class Seasons(str, Enum):
    FRUEHLING = "fruehling"
    SOMMER = "sommer"
    HERBST = "herbst"
    WINTER = "winter"


class Types(str, Enum):
    TRAINING = "training"
    CAMP = "camp"


class TrainingLocation(str, Enum):
    ZAEHRINGEN = "zaehringen"
    UMKIRCH = "umkirch"


class FormTrainingAdult(BaseModel):
    first_name: str = Field(..., description="First name of the person sending the form", example="John")
    last_name: str = Field(..., description="Last name of the person sending the form", example="Doe")
    address: str = Field(..., description="Adress of the person sending the form", example="Teststreet 21")
    city: str = Field(..., description="Name of the city where person lives", example="Freiburg")
    postal_code: str = Field(..., description="Postal code of the city where person lives", example="12354")
    birthday: datetime = Field(..., description="Birthday of the person sending the form", example=datetime.today())
    phone: str = Field(..., description="Phone number of the person sending the form", example="+461234567")
    email: EmailStr = Field(..., description="Email of the person sending the form", example="johndoe@gmail.com")
    age_group: AgeGroup = Field(..., description="The age group of the person", example=AgeGroup.ERWACHSENE)
    type: Types = Field(..., description="What type of of tennis it is", example=Types.CAMP)
    training_time: list[str] = Field(..., description="The hours of trainings you could choose", example=["14-15", "15-16"])
    privacy: bool = Field(..., description="Allow privacy", example=True)
    year: int = Field(..., description="Year in regards to what year the event is taking place in", example=2023)
    season: str = Field(..., description="Season in regards to what season the event is taking place in", example="summer")
    comments: Optional[str] = Field(..., description="Comment from the person sending the from")
    location: TrainingLocation = Field(..., description="The location of training", example=TrainingLocation.UMKIRCH)
    timestamp: datetime = datetime.utcnow()


class FormTrainingChildren(FormTrainingAdult):
    name_parent: str = Field(..., description="Name of parent", example="Maria")
    training_type: list[str] = Field(..., description="The type of trainings you could choose", example=["solo", "group"])


