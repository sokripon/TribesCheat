from typing import Optional

from data.send import world_create
from data.send import world_save
from utils import compression
from data.send import world_stats
import random


def create_default_world(name: Optional[str] = None) -> world_create.Model:
    return world_create.Model(
        GameMode=5,
        Name=name or ("World " + str(random.randint(9258094, 20000000))),
        IsPrivate=False,
        Password="",
        PlayersCount=1,
        Seed=0,
        Config_=world_create.Config(
            MapSize=0,
            BossAddsDifficulty=0,
            NPCDifficulty=0,
            QuestsDifficulty=0,
            EventsDifficulty=0,
            MythBossDifficulty=0,
            CreaturesDifficulty=0,
            MinionsDifficulty=0,
            GiantsDifficulty=0,
            GiantsArrow=0,
            YggdrasilDecay=0,
            DeadLootChest=0,
            XPDifficulty=0,
            LootDifficulty=0,
            SpawnGiants=0,
            SpawnMinions=0,
            GateInitialLevel=0,
            WatchtowerInitialLevel=0,
            PvPMode=0
        )
    )


def create_world_save(world_id: str, **kwargs) -> world_save.Model:
    # Players should not be empty to actually save the player data in the world, but for giving xp it is not needed
    world_data = world_save.UnCompressedData(

        RegisteredPlayers=kwargs.get("RegisteredPlayers", 0),
        GiantLevel=kwargs.get("GiantLevel", 0),
        GiantKillCount=kwargs.get("GiantKillCount", 0),
        SagaBossKillCount=kwargs.get("SagaBossKillCount", 0),
        SagaBossKillIds=kwargs.get("SagaBossKillIds", []),
        SpawnedGiants=kwargs.get("SpawnedGiants", []),
        Players=kwargs.get("Players", []),
        ExitedPlayers=kwargs.get("ExitedPlayers", []),
        WorldCharacters=kwargs.get("WorldCharacters", []),
        Containers=kwargs.get("Containers", []),
        WorldContainers=kwargs.get("WorldContainers", []),
        ConstructionCount=kwargs.get("ConstructionCount", 0),
        Chunks=kwargs.get("Chunks", []),
        Grids=kwargs.get("Grids", []),
        RespawnTimers=kwargs.get("RespawnTimers", []),
        ReplicatedRespawnTimers=kwargs.get("ReplicatedRespawnTimers", []),
        RespawnAnnouncements=kwargs.get("RespawnAnnouncements", []),
        PersistentValues=kwargs.get("PersistentValues", []),
        ReplicatedPersistentValues=kwargs.get("ReplicatedPersistentValues", []),
        Shrines=kwargs.get("Shrines", []),
        GameEvents=kwargs.get("GameEvents", []),
        Quests=kwargs.get("Quests", []),
        Caves=kwargs.get("Caves", []),
        Upgrades=kwargs.get("Upgrades", []),
        Hazards=kwargs.get("Hazards", []),
        ExploredChunksCompressedBytes=kwargs.get("ExploredChunksCompressedBytes", []),
        CurrentlySpawnMinionCount=kwargs.get("CurrentlySpawnMinionCount", 0),
        YggdrasilRemainingHealth=kwargs.get("YggdrasilRemainingHealth", 0),
        ElapsedTime=kwargs.get("ElapsedTime", 0),
        Status=kwargs.get("Status", 0),
        IsBifrostActivated=kwargs.get("IsBifrostActivated", False),
    )
    return world_save.Model(
        DataSize=1,
        CompressedData=compression.compress_to_gzip(world_data.json()),
        URLParams=[world_id]
    )
