from typing import Any

from pydantic import BaseModel, Field


class Model(BaseModel):
    DataSize: int
    CompressedData: list[int]
    URLParams: list[str]


class WorldPosition(BaseModel):
    X: int
    Y: int
    Z: int


class LastKnownPosition(BaseModel):
    X: int
    Y: int
    Z: int


class SpawnedGiant(BaseModel):
    id: str = Field(None, alias="_id")
    GiantId: int
    Health: int
    WorldPosition: WorldPosition
    CurrentTargetIndex: int
    CurrentZoneIndex: int
    GiantCurrentPathIndex: int
    Delay: float
    HasBeenDiscovered: bool
    LastKnownPosition: LastKnownPosition
    class Config:
        allow_population_by_field_name = True

class WorldPosition1(BaseModel):
    X: float
    Y: float
    Z: float


class Item(BaseModel):
    id: str = Field(None, alias="_id")
    ItemId: int
    Durability: int
    class Config:
        allow_population_by_field_name = True

class Slot(BaseModel):
    id: str = Field(None, alias="_id")
    Item: Item
    Count: int
    LoadoutIndex: int
    class Config:
        allow_population_by_field_name = True

class Container(BaseModel):
    id: str = Field(None, alias="_id")
    ContainerId: int
    Type: int
    Slots: list[Slot]
    SelectedLoadout: int
    IsInstanced: bool
    class Config:
        allow_population_by_field_name = True


class RuneStoneGoBackPosition(BaseModel):
    X: int
    Y: int
    Z: int


class RespawnPosition(BaseModel):
    X: int
    Y: int
    Z: int


class Player(BaseModel):
    id: str = Field(None, alias="_id")
    IsAdmin: bool
    IsOnline: bool
    Health: int
    SpecialPoints: int
    SwimStamina: int
    SelectedClass: int
    UnlockedSkills: list
    WishlistedRecipes: list
    PlayerXP: int
    WorldPosition: WorldPosition1
    Containers: list[Container]
    SawFTUE: bool
    RuneStoneGoBackPosition: RuneStoneGoBackPosition
    RuneStoneInGoBackMode: bool
    RuneRemainingCooldown: int
    ConstructionCount: int
    AltarUseCount: int
    PersonalQuests: list[int]
    CurrentSagaQuestFirstStepId: str
    WorbenchId: str
    RespawnPosition: RespawnPosition
    OwnedHazard: list
    class Config:
        allow_population_by_field_name = True


class WorldCharacter(BaseModel):
    id: str = Field(None, alias="_id")
    Type: int
    Cooldown: int
    class Config:
        allow_population_by_field_name = True

class Item1(BaseModel):
    id: str = Field(None, alias="_id")
    ItemId: int
    Durability: int
    class Config:
        allow_population_by_field_name = True


class Slot1(BaseModel):
    id: str = Field(None, alias="_id")
    Item: Item1
    Count: int
    LoadoutIndex: int
    class Config:
        allow_population_by_field_name = True


class Container1(BaseModel):
    id: str = Field(None, alias="_id")
    ContainerId: int
    Type: int
    Slots: list[Slot1]
    SelectedLoadout: int
    IsInstanced: bool
    class Config:
        allow_population_by_field_name = True

class RespawnTimer(BaseModel):
    id: str = Field(None, alias="_id")
    Timer: int
    class Config:
        allow_population_by_field_name = True

class Quest(BaseModel):
    id: str = Field(None, alias="_id")
    QuestDataId: int
    FirstStepId: str
    NextStepId: str
    PlayerId: str
    QuestGiverId: str
    NPCEntityId: str
    Status: int
    Conditions: dict[str, Any]
    Progression: dict[str, Any]
    IsDirty: bool
    CurrentProgression: int
    MaxProgression: int
    ActivationTime: int
    CooldownEndTime: int
    IsSaga: bool
    class Config:
        allow_population_by_field_name = True

class Upgrade(BaseModel):
    id: str = Field(None, alias="_id")
    UpgradeDataId: int
    HighestCompletedUpgradeDataId: int
    ContainerId: str
    class Config:
        allow_population_by_field_name = True

class UnCompressedData(BaseModel):
    RegisteredPlayers: int
    GiantLevel: int
    GiantKillCount: int
    SagaBossKillCount: int
    SagaBossKillIds: list
    SpawnedGiants: list[SpawnedGiant]
    Players: list[Player]
    ExitedPlayers: list
    WorldCharacters: list[WorldCharacter]
    Containers: list[Container1]
    WorldContainers: list
    ConstructionCount: int
    Chunks: list
    Grids: list
    RespawnTimers: list[RespawnTimer]
    ReplicatedRespawnTimers: list
    RespawnAnnouncements: list
    PersistentValues: list
    ReplicatedPersistentValues: list
    Shrines: list
    GameEvents: list
    Quests: list[Quest]
    Caves: list
    Upgrades: list[Upgrade]
    Hazards: list
    ExploredChunksCompressedBytes: list[int]
    CurrentlySpawnMinionCount: int
    YggdrasilRemainingHealth: int
    ElapsedTime: int
    Status: int
    IsBifrostActivated: bool
