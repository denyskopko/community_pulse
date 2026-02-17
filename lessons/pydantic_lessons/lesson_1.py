from pydantic import BaseModel


# class Address(BaseModel):
#     city: str
#     street: str
#     post_code: str
#
#
# class User(BaseModel):
#     id: int
#     name: str
#     age: int
#     is_active: bool
#     address: Address
#
#
# address = Address(
#     city="Warsaw",
#     street="Main Street",
#     post_code="X0-73"
# )
#
# user = User(
#     id=1,
#     name="123123",
#     age=40,
#     is_active=True,
#     address=address
# )
#
#
# print(user)
#
# print(user.address.street)




# ==============================================================================

# JSON with pydantic

# ==============================================================================

# None -> -> null


# class Address(BaseModel):
#     city: str
#     street: str
#     house_number: int
#
#
# class User(BaseModel):
#     name: str
#     age: int
#     email: str
#     address: Address
#
#
# json_data = """{
#     "name": "Dmitry",
#     "age": 26,
#     "email": "qwerty",
#     "address": {
#         "city": "Berlin",
#         "street": "Test street",
#         "house_number": "123"
#     }
# }"""
#
#
# user = User.model_validate_json(json_data)
#
# print(user)





# ==============================================================================

# Inheritance in Pydantic

# ==============================================================================

# import re
# from enum import StrEnum
# from datetime import datetime
#
#
# class TestType(StrEnum):
#     BLOOD = "blood"
#     URINE = "urine"
#     XRAY = "Xray"
#     MRI = "mri"
#
#
# class LabTestBase(BaseModel):
#     patient_id: int
#     test_type: TestType
#     test_date: datetime
#
#
# class LabTestRequest(LabTestBase):
#     notes: str
#
#
# class LabTestResponse(LabTestBase):
#     id: int
#     result: str | None = None
#     is_completed: bool
#
#     def is_urgent(self) -> bool:
#         if not self.result:
#             return False
#
#         if "гемоглобин" in self.result.lower():
#             match_pattern = re.search(r"(\d+)\s*г/л", self.result.lower())
#             if match_pattern:
#                 value = int(match_pattern.group(1))
#                 return value < 90 or value > 160  # value == 85 -> CRITICAL | value == 170 -> CRITICAL
#         return False
#
#
# raw_data = """{
#     "id": 1,
#     "patient_id": 123,
#     "test_type": "blood",
#     "test_date": "2025-01-12T14:58:33",
#     "result": "Гемоглобин: 200 г/л",
#     "is_completed": true
# }"""
#
# response = LabTestResponse.model_validate_json(raw_data)
#
# print(response)
#
# if response.is_urgent():
#     print("НУЖНО СРОЧНОЕ ВМЕШАТЕЛЬСТВО")




# ==============================================================================

# 'Field' function in Pydantic

# ==============================================================================


# from enum import StrEnum
# from pydantic import Field
#
#
# class Roles(StrEnum):
#     BASE = "Base"
#     CLIENT = "Client"
#     ADMIN = "Admin"
#     CLEVEL = "Clevel"
#
#
# class BaseUser(BaseModel):
#     id: int = Field(gt=0)
#     name: str = Field(min_length=2, max_length=25)
#     last_name: str = Field(default='N\\A', min_length=2, max_length=25)
#
#
# class ClientUser(BaseUser):
#     loyalty: int = Field(default=1, ge=1, le=5)
#
# user = BaseUser(id=1, name="Test")
#
# print(user)





# ==============================================================================

# custom validators in Pydantic

# ==============================================================================

# from pydantic import (
#     Field,
#     field_validator,
#     model_validator,
#     BaseModel,
#     EmailStr
# )
#
#
# class User(BaseModel):
#     name: str = Field(min_length=2, max_length=25)
#     age: int = Field(gt=16)
#     # email: str = Field(pattern=r"") option 1
#     email: EmailStr
#
#     # @classmethod
#     # def foo(cls):
#     #     ...
#
#     @field_validator('name')
#     @classmethod
#     def validate_name(cls, value: str) -> str:
#         if not value.isalpha():
#             raise ValueError(
#                 "Name must contain only letters"
#             )
#
#         return value
#
#     @field_validator('email')
#     @classmethod
#     def check_email_domain(cls, value: str) -> str:
#         whitelist = {"icloud.com", "yahoo.com"}
#
#         current_domain = value.split('@')[-1]  # gmail.com
#
#         if current_domain not in whitelist:
#             raise ValueError(
#                 f"Email must be from one of following domains: {', '.join(whitelist)}"
#             )
#         return value
#
#
# data = """{
#     "name": "Anna",
#     "age": 20,
#     "email": "qwerty@icloud.com"
# }
# """
#
#
# user = User.model_validate_json(data)
#
# print(user)




# ==============================================================================

# custom settings in Pydantic, and model_validator

# ==============================================================================

from pydantic import ConfigDict, model_validator
from datetime import datetime



class Event(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,  # глобально убирает все пробелы из строковых значений
        validate_assignment=True,
        json_encoders={
            datetime: lambda v: v.strftime("%Y  -  %m  -  %d  | %H : %M")
        }
    )

    title: str
    description: str
    start_date: datetime
    end_date: datetime

    @model_validator(mode='after')
    def validate_dates(self):
        print("Our processed object")
        print(self)

        if self.start_date > self.end_date:
            raise ValueError(
                "Start date cannot be after end date"
            )
        return self

event_json = """
{
    "title": "  Annual Developer Conference  ",
    "description": " Meet leading software developers from around the world.  ",
    "start_date": "2025-03-13 15:00:00",
    "end_date": "2025-03-13 18:00:00"
}
"""

event = Event.model_validate_json(event_json)


print("PROCESSED EVENT")
# print(event)


print(event.model_dump_json(indent=4))
