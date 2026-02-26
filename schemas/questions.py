from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import datetime

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, # для валидации данных str_strip_whitespace=True,
        str_strip_whitespace=True,#удалить пробелы extra = "forbid"
        extra="forbid"  # запретить лишние поля
    )


class CategoryBase(BaseSchema):
    name: str = Field(min_length=3, max_length=100)


class CategoryResponse(CategoryBase):
    id: int


class QuestionBase(BaseSchema):
    title: str = Field(min_length=15, max_length=150)
    description: str | None = Field(min_length=20, max_length=750, default=None)
    start_date: datetime
    end_date: datetime

    @model_validator(mode="after")
    def validate_date(self):
        if self.start_date > self.end_date:
            raise ValueError("start_date must be before end_date")
        return self


class QuestionCreateRequest(QuestionBase):
    category_id: int


class QuestionUpdateRequest(BaseSchema):
    title: str | None = Field(min_length=15, max_length=150, default=None)
    description: str | None = Field(min_length=20, max_length=750, default=None)
    start_date: datetime | None = None
    end_date: datetime | None = None

    @model_validator(mode="after")
    def validate_date(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValueError("start_date must be before end_date")
        return self


class QuestionRetrieve(QuestionBase):
    id: int
    is_active: bool
    category: CategoryResponse


class QuestionList(BaseSchema):
    id: int
    title: str
    start_date: datetime
    is_active: bool
    category: CategoryResponse


class QuestionCreateResponse(QuestionRetrieve):
    pass








