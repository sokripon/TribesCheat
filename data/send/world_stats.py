from pydantic import BaseModel, Field, Extra


class PlayerStat(BaseModel):
    id: str = Field(None, alias="_id")
    Name: str
    CurrentTotalSeasonXP: int
    Classe: int
    Level: int
    Portrait: int
    XPEarned: int
    CreatureKilled: int
    DamageDealt: int
    HealingDone: int
    AlliesRevived: int
    IngredientHarvested: int
    ItemCrafted: int
    SoulsCollected: int
    SoulsSpent: int
    RunesLooted: int
    GoldenHornsEarned: int
    SeasonXP: int
    DaysSurvived: int
    GiantKillCount: int
    SagaBossKillCount: int
    StatHighlight: int
    IsNotable: bool

    class Config:
        allow_population_by_field_name = True






class WorldStats(BaseModel):
    GameMode: int
    Seed: int
    ElapsedTime: int
    DaysSurvived: int
    GiantKillCount: int
    SagaBossKillCount: int
    PlayerStats: list[PlayerStat]


class Model(BaseModel):
    WorldStats: WorldStats
    URLParams: list[str]
