from pydantic import BaseModel


class Model(BaseModel):
    URLParams: list[str]
    Password: str
