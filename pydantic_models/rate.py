import datetime
from _pydecimal import Decimal

from pydantic import BaseModel, Field, validator, field_validator


class Rate(BaseModel):
    cargo_type: str = Field(example="Glass")
    rate: str = Field(example="0.05")
    date: datetime.date

    @validator("date", pre=True)
    def parse_birthdate(cls, value):
        return datetime.datetime.strptime(
            value,
            "%Y-%m-%d"
        ).date()
