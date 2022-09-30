from pydantic import BaseModel


class Model(BaseModel):
    UseBifrost: bool
    GoldenHornBonus: int
    URLParams: list[str]
