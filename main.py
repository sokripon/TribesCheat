import sys
import time

import httpx
import pymem
from loguru import logger
from pymem.exception import WinAPIError
from pymem.ptypes import RemotePointer

from data.send import world_create as world_create_send, world_stats
from data.receive import world_create as world_create_receive
from data.receive import users_me
from data.send import world_leave as world_leave_send
from data.receive import default_response
from data.send import world_stats as world_stats_send
from data.send import world_save as world_save_send
from data.receive import world_save as world_save_receive
from data.send import users_saveuserdata
from data.send import world_listrewards as world_listrewards_send
from data.receive import world_listrewards as world_listrewards_receive
from data.send import world_join as world_join_send
from data.receive import world_join as world_join_receive
import utils.world


def follow_offsets(process, start: int, offsets: list[int]):
    v = start
    for offset in offsets:
        pointer = RemotePointer(process.process_handle, v)
        val = pointer + offset
        v = val.value
    return v


def get_string_in_memory(process_name: str, module_name: str, offsets: list[int], module_offset: int, size: int) -> str:
    process = pymem.Pymem(process_name)
    start_address = pymem.process.module_from_name(process.process_handle, module_name).lpBaseOfDll
    start = start_address + module_offset
    ticket_address = follow_offsets(process, start, offsets)
    ticket_str = process.read_string(ticket_address, size)
    return ticket_str


def get_int_in_memory(process_name: str, offsets: list[int], start: int) -> int:
    process = pymem.Pymem(process_name)
    offsets = offsets
    start = process.base_address + start
    ticket_address = follow_offsets(process, start, offsets)
    ticket_int = process.read_int(ticket_address)
    return ticket_int


def change_int_in_memory(process_name: str, offsets: list[int], start: int, value: int):
    process = pymem.Pymem(process_name)
    offsets = offsets
    start = process.base_address + start
    ticket_address = follow_offsets(process, start, offsets)
    process.write_int(ticket_address, value)


def get_horn_count():
    return get_int_in_memory("TOM-Win64-Shipping.exe", [0x50, 0x40, 0x1B8, 0x4], 0x0553F670)


def set_horn_count(value: int):
    """
    This will not give you any golden horns!!
    """
    change_int_in_memory("TOM-Win64-Shipping.exe", [0x50, 0x40, 0x1B8, 0x4], 0x0553F670, value)


def get_ticket_from_game_memory():
    import sqlite3
    con = sqlite3.connect("auth_offsets.db")
    cur = con.cursor()
    res = cur.execute(
        "SELECT name, moduleoffset, offset1, offset2, offset3, offset4, offset5, offset6, offset7 FROM results INNER JOIN modules on results.moduleid = modules.moduleid;")
    for a in res.fetchall():
        module_name = a[0]
        module_offset = a[1]
        offsets = [x for x in a[2:][::-1] if x is not None]
        try:
            _return = get_string_in_memory("TOM-Win64-Shipping.exe", module_name, offsets, module_offset,
                                           480)

            logger.success(f"{module_name=} {module_offset=} {offsets=}")
            return _return
        except WinAPIError as e:
            logger.error(f"Offsetswrong: {module_name=} {module_offset=} {offsets=}")
    raise NotImplementedError("No offsets found")


class TribesClient:
    tribes_base_url = "https://api.tribesofmidgard.com/live"
    client_version = "inferno-3.0-11829"
    header_base = {"X-TOM-Client-Version": client_version, "User-Agent": "X-UnrealEngine-Agent",
                   "Content-Type": "application/json", "Accept": "application/json"}
    time_per_day = 600

    def __init__(self, auth_key: str):
        self.auth_key = auth_key
        self.headers = {**self.header_base, "Authorization": auth_key}
        self.player_id = None

    @staticmethod
    def create_with_ticket(ticket: str) -> "TribesClient":
        return TribesClient(TribesClient.get_auth_token_from_ticket(ticket))

    @staticmethod
    def get_auth_token_from_ticket(ticket: str) -> str:
        """
        Get auth token from ticket
        :param ticket: 400-500 character string used to get an auth token
        :return: auth token: auth token used to authenticate with the tribes of midgard api
        """
        url = TribesClient.tribes_base_url + "/users/auth/steam"
        body = {"Ticket": ticket}
        response = httpx.post(url, headers=TribesClient.header_base, json=body, verify=False)
        if response.status_code != 200:
            raise ValueError(f"Failed to get auth token from ticket. Status code: {response.status_code}")
        return response.json()["Data"]["token"]

    def create_world(self, world: world_create_send.Model) -> world_create_receive.Model:
        url = TribesClient.tribes_base_url + "/world/create"
        response = httpx.post(url, headers=self.headers, json=world.dict(by_alias=True), verify=False)
        if response.status_code != 200:
            raise ValueError(f"Failed to create world. Status code: {response.status_code}")
        return world_create_receive.Model(**response.json())

    def get_user_info(self) -> users_me.Model:
        url = TribesClient.tribes_base_url + "/users/me"
        response = httpx.get(url, headers=self.headers, verify=False)
        if response.status_code != 200:
            raise ValueError(f"Failed to get user info. Status code: {response.status_code}")
        return users_me.Model(**response.json())

    def save_stats(self, stats: world_stats_send.Model) -> default_response.Model:
        url = TribesClient.tribes_base_url + "/world/stats/" + stats.URLParams[0]
        response = httpx.post(url, headers=self.headers, json=stats.dict(by_alias=True), verify=False)
        if response.status_code != 200:
            raise ValueError(f"Failed to save stats. Status code: {response.status_code}")
        return default_response.Model(**response.json())

    def leave_world(self, additional_leave_info: world_leave_send.Model) -> default_response.Model:
        url = TribesClient.tribes_base_url + "/world/leave/" + additional_leave_info.URLParams[0]
        response = httpx.post(url, headers=self.headers, json=additional_leave_info.dict(by_alias=True), verify=False)
        if response.status_code != 200:
            raise ValueError(f"Failed to leave world. Status code: {response.status_code}")
        return default_response.Model(**response.json())

    def save_world(self, world_save: world_save_send.Model) -> world_save_receive.Model:
        url = TribesClient.tribes_base_url + "/world/save/" + world_save.URLParams[0]
        response = httpx.post(url, headers=self.headers, json=world_save.dict(by_alias=True), verify=False)
        if response.status_code != 200:
            raise ValueError(f"Failed to save world. Status code: {response.status_code}")
        return world_save_receive.Model(**response.json())

    def save_user(self, user_data: users_saveuserdata.Model) -> default_response.Model:
        url = TribesClient.tribes_base_url + "/users/saveuserdata"
        response = httpx.post(url, headers=self.headers, json=user_data.dict(by_alias=True), verify=False)
        if response.status_code != 200:
            raise ValueError(f"Failed to save user. Status code: {response.status_code}")
        return default_response.Model(**response.json())

    def list_rewards(self, list_rewards: world_listrewards_send.Model) -> world_listrewards_receive.Model:

        url = TribesClient.tribes_base_url + "/world/listrewards/" + list_rewards.URLParams[0]
        response = httpx.post(url, headers=self.headers, json=list_rewards.dict(by_alias=True), verify=False)
        if response.status_code != 200:
            raise ValueError(f"Failed to list rewards. Status code: {response.status_code}")
        return world_listrewards_receive.Model(**response.json())

    def join_world(self, join_world: world_join_send.Model) -> world_join_receive.Model:
        url = TribesClient.tribes_base_url + "/world/join/" + join_world.URLParams[0]
        response = httpx.post(url, headers=self.headers, json=join_world.dict(by_alias=True), verify=False)
        if response.status_code != 200:
            raise ValueError(f"Failed to join world. Status code: {response.status_code}")
        return world_join_receive.Model(**response.json())


def logged_input(prompt: str) -> str:
    logger.info(prompt)
    return input("").strip()


def main():
    auth_token = None
    days = 1
    elapsed_time = TribesClient.time_per_day * days
    level = 1
    saga_boss_kills = 0
    giant_boss_kills = 0
    logger.remove()
    logger.add(sys.stdout, colorize=True, enqueue=False)
    logger.info("Starting")

    if auth_token is None:
        logger.info(
            "Auth-token look like this: 'Bearer <token>', example: 'Bearer eyJhbGciOiJ'(In reality it's much longer)")
        auth_token = logged_input(
            "Please enter your auth token or start the game and press enter to search for it in memory: ")
        if auth_token == "":
            logger.info("Searching for ticket(we will get the auth-token through this) in memory")
            ticket = get_ticket_from_game_memory()
            logger.success(f"Found ticket!")
            auth_token = TribesClient.get_auth_token_from_ticket(ticket)
            logger.success(f"Got auth-token from ticket")

    tribes_client = TribesClient(auth_token)
    logger.info("Created tribes client")
    user_info_start = tribes_client.get_user_info()
    user_info = user_info_start
    logger.info(
        f"Got user info before: {user_info_start.Data.Currencies[1]} golden horns, {user_info_start.Data.SeasonXP} season xp")
    user_endless_horns = logged_input(
        "Endless horns? (this will keep setting your horns to 99, your game will show a lower horn count, but you can still buy in the shop!)(y/n)(default=n): ") == "y"
    if user_endless_horns:
        user_golden_horns = 99
        user_season_xp = 0
    else:
        user_golden_horns = int(
            logged_input("Please enter how many golden horns you want to receive(max is 99)(default=0): ") or 0)
        user_season_xp = int(logged_input("Please enter how much season xp you want to receive(default=0): ") or 0)
    while True:
        default_world = utils.world.create_default_world()
        world = tribes_client.create_world(default_world)
        logger.info(f"Created world: {world.Data.Name}")
        world_saved = utils.world.create_world_save(world.Data.id, ElapsedTime=elapsed_time,
                                                    SagaBossKillCount=saga_boss_kills, GiantKillCount=giant_boss_kills)
        world_saved = tribes_client.save_world(world_saved)
        logger.info(f"World saved")
        player_save_stats = world_stats.PlayerStat(id=world.Data.UsersInfos[0].id, Name="",
                                                   CurrentTotalSeasonXP=user_info_start.Data.SeasonXP + user_season_xp,
                                                   Classe=99, Level=level, Portrait=0, XPEarned=0, CreatureKilled=0,
                                                   DamageDealt=0, HealingDone=0, AlliesRevived=0, IngredientHarvested=0,
                                                   ItemCrafted=0, SoulsCollected=10, SoulsSpent=0, RunesLooted=0,
                                                   GoldenHornsEarned=user_golden_horns,
                                                   SeasonXP=user_season_xp,
                                                   DaysSurvived=days,
                                                   GiantKillCount=giant_boss_kills, SagaBossKillCount=saga_boss_kills,
                                                   StatHighlight=49, IsNotable=False)
        world_save_stats = world_stats.WorldStats(GameMode=5, Seed=world.Data.Seed, ElapsedTime=elapsed_time,
                                                  DaysSurvived=days, GiantKillCount=giant_boss_kills,
                                                  SagaBossKillCount=saga_boss_kills,
                                                  PlayerStats=[player_save_stats])
        a = tribes_client.save_stats(world_stats.Model(WorldStats=world_save_stats, URLParams=[world.Data.id]))
        logger.info(f"World stats saved")
        c = tribes_client.leave_world(
            additional_leave_info=world_leave_send.Model(UseBifrost=True,
                                                         GoldenHornBonus=user_golden_horns,
                                                         URLParams=[world.Data.id]))
        logger.info(f"Left world: {world.Data.Name}")
        user_info = tribes_client.get_user_info()
        logger.success(
            f"Got new user info: {user_info.Data.Currencies[1]} golden horns, {user_info.Data.SeasonXP} season xp")
        if user_endless_horns:
            while tribes_client.get_user_info().Data.Currencies[1] == 99:
                time.sleep(1)
            logger.info("Detected lower horn count, setting to 99")
            set_horn_count(99)
        else:
            break


if __name__ == "__main__":
    main()
