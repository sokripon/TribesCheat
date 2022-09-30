from pydantic import BaseModel, Field


class Data(BaseModel):
    Success: bool = Field(None, alias="success")


class Model(BaseModel):
    Data: Data
    Messages: list
