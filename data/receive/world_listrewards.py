from pydantic import BaseModel, Field


class Player(BaseModel):
    Name: str
    Portrait: int
    Classe: int
    Level: int
    XPEarned: int
    SeasonXP: int
    CurrentTotalSeasonXP: int
    DaysSurvived: int
    GiantKillCount: int
    SagaBossKillCount: int
    LeaveWorldTimestamp: int
    id: str = Field(None, alias="_id")
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
    StatHighlight: int
    IsNotable: bool


class Records(BaseModel):
    PlayerXPRecord: int
    GiantsKilledRecord: int
    DaysSurvivedRecord: int
    GoldenHornsRecord: int
    SagaBossesKilledRecord: int
    CreatureKilledRecord: int
    DamageDealtRecord: int
    HealingDoneRecord: int
    AlliesRevivedRecord: int
    IngredientHarvestedRecord: int
    ItemCraftedRecord: int
    SoulCollectedRecord: int
    SoulSpentRecord: int
    RunesLootedRecord: int


class Data(BaseModel):
    DaysSurvived: int
    GiantKillCount: int
    SagaBossKillCount: int
    GameMode: int
    Seed: int
    Time: int
    Players: list[Player]
    XPMultiplierGlobal: float
    PlayerXPEarned: int
    IsVictory: bool
    GoldenHorns: int
    Records: Records


class Model(BaseModel):
    Data: Data
    Messages: list
