import random
from typing import List, Union, Optional

import httpx
import pymem
from loguru import logger
from pydantic import BaseModel
from pymem.ptypes import RemotePointer


def follow_offsets(process, start: int, offsets: list[int]):
    v = start
    for offset in offsets:
        pointer = RemotePointer(process.process_handle, v)
        val = pointer + offset
        v = val.value
    return v


class Avatar(BaseModel):
    Emotes: List[int]
    Commands: List[int]
    Transmogs: List[int]
    _id: str
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
    __v: int
    StarterKit: Optional[int]
    DeathChestId: int


class UserData(BaseModel):
    CompletedChallenges: List[int]
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


class PlayerInfo(BaseModel):
    id: str
    Platform: int
    Currencies: List[int]
    PurchasedCosmetics: List[int]
    Avatar: Avatar
    XP: int
    SeasonXP: int
    Name: str
    ContentBundles: List[Union[int, str]]
    ClaimedChallenges: List[int]
    UnlockedBlueprints: List[int]
    OwnedEntitlements: List[int]
    UserData: UserData
    currencyCode: str


class TribeClient:
    tribes_base_url = "https://api.tribesofmidgard.com/live"
    client_version = "serpent-2.02-5037"
    header_base = {
        "X-TOM-Client-Version": client_version,
        "User-Agent": "X-UnrealEngine-Agent",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, auth_key: str):
        self.auth_key = auth_key
        self.headers = {**self.header_base, "Authorization": f"Bearer {auth_key}"}
        self.player_id = None

    @staticmethod
    def get_auth_token_from_ticket(ticket: str) -> str:
        url = TribeClient.tribes_base_url + "/users/auth/steam"
        body = {
            "Ticket": ticket
        }
        response = httpx.post(url, headers=TribeClient.header_base, json=body)
        return response.json()["Data"]["token"]

    @staticmethod
    def get_ticket_from_game_memory():
        auth_size = 480  # The size of the needed string
        process = pymem.Pymem('TOM-Win64-Shipping.exe')
        offsets = [0x30, 0x18, 0x38, 0x28, 0x338, 0x0]
        start = process.base_address + 0x0508D588
        ticket_address = follow_offsets(process, start, offsets)
        ticket_str = process.read_string(ticket_address, auth_size)
        return ticket_str

    def player_info(self) -> PlayerInfo:
        url = self.tribes_base_url + "/users/me"
        response = httpx.get(url, headers=self.headers)
        response_json = response.json()["Data"]
        player_id = response_json["id"]
        self.player_id = player_id

        return PlayerInfo(**response_json)

    def create_world(self):
        url = self.tribes_base_url + "/world/create"
        world_name = "World " + str(random.randint(9258094, 20000000))
        body = {
            "GameMode": 5,
            "Name": world_name,
            "IsPrivate": False,
            "Password": "",
            "PlayersCount": 1,
            "Seed": 0,
            "Config": {
                "MapSize": 0,
                "BossAddsDifficulty": 0,
                "NPCDifficulty": 0,
                "QuestsDifficulty": 0,
                "EventsDifficulty": 0,
                "MythBossDifficulty": 0,
                "CreaturesDifficulty": 0,
                "MinionsDifficulty": 0,
                "GiantsDifficulty": 0,
                "GiantsArrow": 0,
                "YggdrasilDecay": 0,
                "DeadLootChest": 0,
                "XPDifficulty": 0,
                "LootDifficulty": 0,
                "SpawnGiants": 0,
                "SpawnMinions": 0,
                "GateInitialLevel": 1,
                "WatchtowerInitialLevel": 0
            }
        }
        response = httpx.post(url, headers=self.headers, json=body)
        response_json = response.json()["Data"]
        world_id = response_json["_id"]
        return world_id

    def save_world(self, world_id: str, elapsed_time: int = 20000, bosses_slain: int = 1,
                   player_experience: int = 1000):
        """

        :param world_id:
        :param elapsed_time:
        :param bosses_slain: Needs to be 1 or more, gives 5 golden horns per boss
        :param player_experience:
        :return:
        """
        url = self.tribes_base_url + "/world/save/" + world_id
        bosses_slain = max(bosses_slain, 1)
        body = {
            "Data": {
                "RegisteredPlayers": 0,
                "GiantLevel": 0,
                "SagaBossKillCount": bosses_slain,
                "SagaBossKillIds": [],
                "SpawnedGiants": [],
                "Players": [
                    {
                        "_id": self.player_id,
                        "IsAdmin": True,
                        "IsOnline": False,
                        "Health": 3000,
                        "SpecialPoints": 90,
                        "SelectedClass": 254,
                        "UnlockedSkills": [],
                        "WishlistedRecipes": [],
                        "PlayerXP": player_experience,
                        "WorldPosition": {
                            "X": -2531.97509765625,
                            "Y": 6664.96630859375,
                            "Z": 392.1499938964844
                        },
                        "Containers": [],
                        "SawFTUE": False,
                        "RuneStoneGoBackPosition": {
                            "X": 0,
                            "Y": 0,
                            "Z": 0
                        },
                        "RuneStoneInGoBackMode": False,
                        "RuneRemainingCooldown": 0,
                        "ConstructionCount": 0,
                        "AltarUseCount": 0,
                        "PersonalQuests": [],
                        "CurrentSagaQuestFirstStepId": "sagaquest103"
                    }
                ],
                "ExitedPlayers": [],
                "WorldCharacters": [],
                "Containers": [],
                "WorldContainers": [],
                "ConstructionCount": 0,
                "Chunks": [],
                "RespawnTimers": [],
                "ReplicatedRespawnTimers": [],
                "Shrines": [],
                "GameEvents": [],
                "Quests": [
                    {
                        "_id": "sagaquest101",
                        "QuestDataId": 101,
                        "FirstStepId": "sagaquest101",
                        "NextStepId": "",
                        "PlayerId": "",
                        "QuestGiverId": "",
                        "NPCEntityId": "",
                        "Status": 2,
                        "Conditions": {},
                        "Progression": {},
                        "IsDirty": False,
                        "CurrentProgression": 0,
                        "MaxProgression": 0,
                        "ActivationTime": 0,
                        "CooldownEndTime": 0,
                        "IsSaga": True
                    },
                    {
                        "_id": "sagaquest102",
                        "QuestDataId": 102,
                        "FirstStepId": "sagaquest102",
                        "NextStepId": "sagaquest6",
                        "PlayerId": "",
                        "QuestGiverId": "",
                        "NPCEntityId": "",
                        "Status": 3,
                        "Conditions": {},
                        "Progression": {},
                        "IsDirty": False,
                        "CurrentProgression": 0,
                        "MaxProgression": 0,
                        "ActivationTime": 0,
                        "CooldownEndTime": 0,
                        "IsSaga": True
                    },
                    {
                        "_id": "sagaquest6",
                        "QuestDataId": 6,
                        "FirstStepId": "sagaquest102",
                        "NextStepId": "",
                        "PlayerId": "",
                        "QuestGiverId": "",
                        "NPCEntityId": "",
                        "Status": 2,
                        "Conditions": {},
                        "Progression": {},
                        "IsDirty": False,
                        "CurrentProgression": 0,
                        "MaxProgression": 0,
                        "ActivationTime": 0,
                        "CooldownEndTime": 0,
                        "IsSaga": True
                    },
                    {
                        "_id": "sagaquest103",
                        "QuestDataId": 103,
                        "FirstStepId": "sagaquest103",
                        "NextStepId": "sagaquest107",
                        "PlayerId": "",
                        "QuestGiverId": "",
                        "NPCEntityId": "",
                        "Status": 3,
                        "Conditions": {},
                        "Progression": {},
                        "IsDirty": False,
                        "CurrentProgression": 0,
                        "MaxProgression": 0,
                        "ActivationTime": 0,
                        "CooldownEndTime": 0,
                        "IsSaga": True
                    },
                    {
                        "_id": "sagaquest107",
                        "QuestDataId": 107,
                        "FirstStepId": "sagaquest103",
                        "NextStepId": "",
                        "PlayerId": "",
                        "QuestGiverId": "",
                        "NPCEntityId": "",
                        "Status": 2,
                        "Conditions": {},
                        "Progression": {},
                        "IsDirty": True,
                        "CurrentProgression": 0,
                        "MaxProgression": 0,
                        "ActivationTime": 0,
                        "CooldownEndTime": 0,
                        "IsSaga": True
                    },
                    {
                        "_id": "sagaquest105",
                        "QuestDataId": 105,
                        "FirstStepId": "sagaquest105",
                        "NextStepId": "",
                        "PlayerId": "",
                        "QuestGiverId": "",
                        "NPCEntityId": "",
                        "Status": 2,
                        "Conditions": {},
                        "Progression": {},
                        "IsDirty": False,
                        "CurrentProgression": 0,
                        "MaxProgression": 0,
                        "ActivationTime": 0,
                        "CooldownEndTime": 0,
                        "IsSaga": True
                    },
                    {
                        "_id": "sagaquest111",
                        "QuestDataId": 111,
                        "FirstStepId": "sagaquest111",
                        "NextStepId": "sagaquest112",
                        "PlayerId": "",
                        "QuestGiverId": "",
                        "NPCEntityId": "",
                        "Status": 3,
                        "Conditions": {},
                        "Progression": {},
                        "IsDirty": False,
                        "CurrentProgression": 0,
                        "MaxProgression": 0,
                        "ActivationTime": 0,
                        "CooldownEndTime": 0,
                        "IsSaga": True
                    },
                    {
                        "_id": "sagaquest112",
                        "QuestDataId": 112,
                        "FirstStepId": "sagaquest111",
                        "NextStepId": "",
                        "PlayerId": "",
                        "QuestGiverId": "",
                        "NPCEntityId": "",
                        "Status": 2,
                        "Conditions": {},
                        "Progression": {},
                        "IsDirty": False,
                        "CurrentProgression": 0,
                        "MaxProgression": 0,
                        "ActivationTime": 0,
                        "CooldownEndTime": 0,
                        "IsSaga": True
                    }
                ],
                "Caves": [],
                "Upgrades": [],
                "Hazards": [],
                "ExploredChunksCompressedBytes": [],
                "CurrentlySpawnMinionCount": 0,
                "YggdrasilRemainingHealth": 5991,
                "ElapsedTime": elapsed_time,
                "Status": 0,
                "IsBifrostActivated": False
            },
            "URLParams": [
                world_id
            ]
        }
        # Note: maybe get rid of Quests
        response = httpx.post(url, headers=self.headers, json=body)

    def save_user_data(self):
        url = self.tribes_base_url + "/users/saveuserdata"
        # Note: seems not to be needed
        raise NotImplementedError

    def join_world(self, world_id: str):
        url = self.tribes_base_url + "/world/join/" + world_id
        # Note: seems not to be needed
        body = {
            "URLParams": [
                world_id
            ],
            "Password": ""
        }
        response = httpx.post(url, headers=self.headers, json=body)

    def list_rewards(self, world_id: str):
        url = self.tribes_base_url + "/world/listrewards/" + world_id
        # Note: seems not to be needed
        body = {
            "URLParams": [
                world_id
            ],
            "UseBifrost": True,
            "GoldenHornBonus": 0
        }
        response = httpx.post(url, headers=self.headers, json=body)

    def leave_world(self, world_id: str, bonus_golden_horn: int = 0):
        url = self.tribes_base_url + "/world/leave/" + world_id
        body = {
            "UseBifrost": True,
            "GoldenHornBonus": bonus_golden_horn,  # Note: Slain_bosses multiplied by 5
            "URLParams": [
                world_id
            ]
        }
        response = httpx.post(url, headers=self.headers, json=body)
        return response


if __name__ == "__main__":
    slayed_bosses = 1
    elapsed_time = 1000
    player_experience = 1000
    bonus_golden_horns = 95
    auth_token = None

    if not auth_token:
        user_input = input(
            "Please enter your auth token or start the game and press enter to search for it in memory: ")
        auth_token = auth_token if user_input else None
    if not auth_token:
        logger.info(
            "No auth token provided, trying to get it from the game memory(make sure that the game is running!)")
        ticket = TribeClient.get_ticket_from_game_memory()
        logger.info(f"Got ticket!")
        auth_token = TribeClient.get_auth_token_from_ticket(ticket)
        logger.info(f"Got auth token!")

    player = TribeClient(auth_key=auth_token.split(" ")[1])
    logger.info(f"Created client")
    before_player_info = player.player_info()
    logger.info(f"Got id({before_player_info.id}) for player {before_player_info.Name}")
    logger.info(f"Player has {before_player_info.Currencies[1]} golden horns and {before_player_info.XP} XP")
    current_world_id = player.create_world()
    logger.info(f"Created world with id {current_world_id}")
    input_slayed_bosses = input(
        f"How many bosses should be slain?(Every boss gains you 5 horns) (default: {slayed_bosses}) ")
    input_elapsed_time = input(f"How much time should pass? (default: {elapsed_time}) ")
    input_player_experience = input(f"How much experience do you want to receive? (default: {player_experience}) ")
    input_bonus_golden_horns = input(f"How many golden horn do you want to receive? (default: {bonus_golden_horns}) ")
    if input_slayed_bosses:
        slayed_bosses = int(input_slayed_bosses)
    if input_elapsed_time:
        elapsed_time = int(input_elapsed_time)
    if input_player_experience:
        player_experience = int(input_player_experience)
    if input_bonus_golden_horns:
        bonus_golden_horns = int(input_bonus_golden_horns)

    player.save_world(world_id=current_world_id, elapsed_time=elapsed_time, bosses_slain=slayed_bosses,
                      player_experience=player_experience)

    logger.info(f"Saved world with id {current_world_id}")
    player.leave_world(world_id=current_world_id, bonus_golden_horn=bonus_golden_horns)
    logger.info(f"Left world with id {current_world_id}")
    after_player_info = player.player_info()
    logger.info(f"Player has {after_player_info.Currencies[1]} golden horns and {after_player_info.XP} XP")
    logger.success(f"Player earned {after_player_info.Currencies[1] - before_player_info.Currencies[1]} golden horns")
    logger.success(f"Player earned {after_player_info.XP - before_player_info.XP} XP")
