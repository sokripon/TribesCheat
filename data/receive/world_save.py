from typing import Optional
from pydantic import BaseModel, Field


class UsersInfo(BaseModel):
    GoldenHornAmount: int
    id: str = Field(None, alias="_id")
    Name: str
    XP: Optional[int]
    IconId: int
    PlatformUserId: str
    PlatformId: int


class Data(BaseModel):
    UsersInfos: list[UsersInfo]


class Model(BaseModel):
    Data: Data
    Messages: list
