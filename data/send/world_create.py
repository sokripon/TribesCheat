from pydantic import BaseModel, Field


class Config(BaseModel):
    MapSize: int
    BossAddsDifficulty: int
    NPCDifficulty: int
    QuestsDifficulty: int
    EventsDifficulty: int
    MythBossDifficulty: int
    CreaturesDifficulty: int
    MinionsDifficulty: int
    GiantsDifficulty: int
    GiantsArrow: int
    YggdrasilDecay: int
    DeadLootChest: int
    XPDifficulty: int
    LootDifficulty: int
    SpawnGiants: int
    SpawnMinions: int
    GateInitialLevel: int
    WatchtowerInitialLevel: int
    PvPMode: int


class Model(BaseModel):
    GameMode: int
    Name: str
    IsPrivate: bool
    Password: str
    PlayersCount: int
    Seed: int
    Config_: Config = Field(None, alias="Config")
    class Config:
        allow_population_by_field_name = True
