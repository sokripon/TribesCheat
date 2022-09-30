from typing import Any

from pydantic import BaseModel, Field


class Config(BaseModel):
    MapSize: int
    BossAddsDifficulty: int
    NPCDifficulty: int
    QuestsDifficulty: int
    EventsDifficulty: int
    CreaturesDifficulty: int
    MinionsDifficulty: int
    XPDifficulty: int
    GiantsDifficulty: int
    MythBossDifficulty: int
    GiantsArrow: int
    YggdrasilDecay: int
    LootDifficulty: int
    DeadLootChest: int
    SpawnGiants: int
    SpawnMinions: int
    GateInitialLevel: int
    WatchtowerInitialLevel: int
    PvPMode: int


class Player(BaseModel):
    UnlockedSkills: list
    AltarUseCount: int
    id: str = Field(None, alias="_id")
    IsAdmin: bool
    Containers: list


class WorldContent(BaseModel):
    ExploredChunksCompressedBytes: list
    ElapsedTime: int
    Status: int
    SagaBossKillCount: int
    Players: list[Player]
    WorldCharacters: list
    SpawnedGiants: list
    Containers: list
    WorldContainers: list
    Creatures: list
    MaterialSources: list
    Fortifications: list
    Hazards: list


class ServerInfos(BaseModel):
    GameLiftPlacementId: Any
    StartTime: int
    IsOnline: bool
    RegionName: str
    IsBooting: bool
    Status: str
    LatencyInfos: list


class UsersInfo(BaseModel):
    GoldenHornAmount: int
    id: str = Field(None, alias="_id")
    Name: str
    XP: int
    IconId: int
    PlatformUserId: str
    PlatformId: int


class WorldStats(BaseModel):
    DaysSurvived: int
    GiantKillCount: int
    SagaBossKillCount: int
    ElapsedTime: int
    GameMode: int
    Seed: int
    Time: int
    PlayerStats: list


class Data(BaseModel):
    BannedUsers: list
    ClientVersion: str
    id: str = Field(None, alias="_id")
    GameMode: int
    Name: str
    CrossplayGroup: int
    Config_: Config = Field(None, alias="Config")
    MaxPlayers: int
    IsPrivate: bool
    Password: str
    Seed: int
    DayDuration: int
    StartingDayTime: int
    WorldContent: WorldContent
    ServerInfos: ServerInfos
    UsersInfos: list[UsersInfo]
    IsFull: bool
    WorldStats: WorldStats
    createdAt: str
    updatedAt: str
    v: int = Field(None, alias="__v")


class Model(BaseModel):
    Data: Data
    Messages: list
