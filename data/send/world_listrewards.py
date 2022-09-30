from pydantic import BaseModel


class Model(BaseModel):
    URLParams: list[str]
    UseBifrost: bool
    GoldenHornBonus: int
