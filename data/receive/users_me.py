from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Avatar(BaseModel):
    Emotes: list[int]
    Commands: list[int]
    Transmogs: list[int]
    id: str = Field(None, alias='_id')
    UserId: str
    CharacterId: int
    Gender: int
    PetId: int
    SkinToneId: int
    HairColorId: int
    HeadCosmeticId: int
    HaircutCosmeticId: int
    IconId: int
    createdAt: str
    updatedAt: str
    v: int = Field(None, alias='__v')
    StarterKit: Optional[int]
    DeathChestId: int
    class Config:
        allow_population_by_field_name = True


class UserData(BaseModel):
    CompletedChallenges: list[int]
    HasSeenTutorial: bool
    TotalSoulsCollected: int
    TotalSoulsGiven: int
    TotalSoulsSpent: int
    HasMaxedSharpshooter: int
    HasMaxedScout: int
    HasMaxedFighter: int
    HasMaxedBerserker: int
    HasMaxedGuardian: int
    HasMaxedSentinel: int
    HasMaxedWarden: int
    HasMaxedSeer: int
    MaxUserLevelReached: int
    HasRevivedPlayer: int
    HasRevivedNPC: int
    HasCompletedSeason: int
    HasKillGiantIce: int
    HasKillGiantFire: int
    HasKillGiantThunder: int
    HasKillGiantDark: int
    HasKillMythBoss: int
    HasCompletedTutorial: int
    SurvivedDaysInEndless: int
    ConstructionsCountInCreative: int
    HasCraftCommon: int
    HasCraftUncommon: int
    HasCraftRare: int
    HasCraftEpic: int
    HasCraftLegendary: int
    HasCraftMythic: int
    MaxSoulCount: int
    HasPet: int
    BifrostUseCount: int
    NoDeathSessionCount: int
    FastKillEnemyCount: int
    FenrirKillCount: int
    JormungandrKillCount: int
    JormungandrKillTime: int
    RevealedAllShrineCount: int
    FinishWithoutLowHealthCount: int
    SurvivedDaysInSeason: int
    FenrirEnragedKillTime: int
    FenrirSummonerKillTime: int
    MaxMythBossKillInASession: int
    ShrineActivatedInASession: int
    LatestSagaNewsPopup: int
    SurtrKillCount: int
    SurtrKillTime: int
    HasDefeatFenrirSurvival: int
    HasDefeatJormungandrSurvival: int
    HasDefeatSurtrSurvival: int
    HasDefeatGiantIceSurvival: int
    HasDefeatGiantFireSurvival: int
    HasDefeatGiantThunderSurvival: int
    HasDefeatGiantDarkSurvival: int
    WarriorMasteryOneCounter: int
    BerserkerMasteryOneCounter: int
    RangerMasteryOneCounter: int
    HunterMasteryOneCounter: int
    GuardianMasteryOneCounter: int
    SentinelMasteryOneCounter: int
    SeerMasteryOneCounter: int
    WardenMasteryOneCounter: int
    HasCraftCommonStationSurvival: int
    HasCraftUncommonStationSurvival: int
    HasCraftRareStationSurvival: int
    HasCraftEpicStationSurvival: int
    HasPlaceBoatSurvival: int
    HasPlaceShrineSurvival: int
    HasClaimBedSurvival: int
    HasEquipFiveSameRunesSurvival: int
    HarvestedFishCountSurvival: int
    BranchAddedToBonfireCount: int
    CompletedTutorialIds: list


class Data(BaseModel):
    id: str
    Platform: int
    Currencies: list[int]
    PurchasedCosmetics: list[int]
    Avatar: Avatar
    XP: Optional[int]
    SeasonXP: int
    Name: str
    ContentBundles: list[int]
    ClaimedChallenges: list[int]
    UnlockedBlueprints: list[int]
    OwnedEntitlements: list[int]
    UserData: UserData
    currencyCode: str


class Model(BaseModel):
    Data: Data
    Messages: list
