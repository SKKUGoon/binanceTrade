from settings import sysmsg as sysmsgs
from settings import _global_ as const
from settings import color as bc
from settings import table
from dbms.Ddbms import LocalDBMethods

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


PREFIX = "!"
BOT = commands.Bot(command_prefix=PREFIX)
server = LocalDBMethods()


def get_token(target:str, typ:str, loc='..\key.json') -> str:
    if platform.system() == 'Windows':
        pass
    else:
        loc = '/home/goon/crypto/binanceTrade/key.json'
    with open(loc, 'r') as file:
        dat = json.load(file)
    file.close()
    return dat[target][typ]


async def on_ready():
    game = discord.Game("Booted Up")
    await BOT.change_presence(
        status=discord.Status.online,
        activity=game
    )
    print(sysmsgs.BACK03_DISCORD_READY)


async def on_message(message):
    if message.author.BOT:
        return None

    await BOT.process_commands(message)


@BOT.command(name='connection')
async def connection_check(ctx):
    # await ctx.channel.send("")
    print(ctx.command)
    dt = datetime.now().strftime('D%Y%m%dT%H:%M:%S')


@BOT.command(name='restart')
async def connection_restart(ctx):
    print(ctx.command)


@BOT.command(name='trade')
async def report_trade(ctx):
    print(ctx.command)


async def test(ctx):
    print('ping')


if __name__ == "__main__":
    # chat = TradeReport()
    # chat.BOT.run(get_token('discord', 'bot_token'))
    # asyncio.get_event_loop().run_until_complete(listen())
    BOT.run(get_token('discord', 'bot_token'))