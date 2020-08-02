from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date


class User(BaseModel):
    name: str = Field(..., example="Иванов И. И.", title="ФИО пользователя")
    id: int = Field(..., example=42, title="Идентификатор пользователя")
    date_start: Optional[date] = Field(example="2020-02-23", title="Начальная дата")
    date_finish: Optional[date] = Field(example="2020-03-08", title="Конечная дата")


class UserList(BaseModel):
    users: List[User] = []
    count: int = Field(..., example=10, title="Количество пользователей в списке")
