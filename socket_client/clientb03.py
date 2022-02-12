from dbms.Ddbms import LocalDBMethods
from socket_client import clienttree
from settings import sysmsg as sysmsgs
from settings import _global_ as const
from settings import color as bc
from settings import table

from discord.ext import commands
import discord

from datetime import datetime
import asyncio
import platform
import time
import json
import os


# BACK OFFICE CLIENT
# NAME:
# DISCORD CONNECTOR
# OBJECTIVE:
# Get Messages and Record it in Database
# FREQ: On request

def get_token(target: str, typ: str, loc='..\key.json') -> str:
    if platform.system() == 'Windows':
        pass
    else:
        loc = '/home/goon/crypto/binanceTrade/key.json'
    with open(loc, 'r') as file:
        dat = json.load(file)
    file.close()
    return dat[target][typ]


def db_addr():
    if platform.system() == 'Windows':
        return '../TDB.db'
    else:
        return '/home/goon/crypto/binanceTrade/TDB.db'


class CryptoChat(discord.Client):
    PREFIX = "!"
    BOT = commands.Bot(command_prefix=PREFIX)
    server = LocalDBMethods(db_addr())
    server.set_wal()

    async def on_ready(self):
        game = discord.Game("Booted Up")
        await self.BOT.change_presence(
            status=discord.Status.online,
            activity=game
        )
        print(sysmsgs.BACK03_DISCORD_READY)


    async def on_message(self, message):
        if message.author.BOT:
            return None

        await self.BOT.process_commands(message)

    @staticmethod
    @BOT.command(name='connection')
    async def connection_check(ctx):
        # await ctx.channel.send("")
        print(ctx.command)


    @staticmethod
    @BOT.command(name='restart')
    async def connection_restart(ctx):
        print(ctx.command)

    @staticmethod
    @BOT.command(name='trade')
    async def report_trade(ctx):
        print(ctx.command)

    @staticmethod
    async def test(ctx):
        print('ping')


if __name__ == "__main__":
    chat = CryptoChat()
    chat.BOT.run(get_token('discord', 'bot_token'))
