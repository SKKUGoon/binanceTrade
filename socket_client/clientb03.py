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


def process_msg(message:[tuple], normal:bool) -> str:
    if len(message) > 0:
        if normal is True:
            w = [
                "Most Recent Check-in",
                f"date:{message[0][0]}",
                f"time:{message[0][1]}",
                f"status:{message[0][2]}"
            ]
        else:
            w = [
                "Recent Error Occured at",
                f"date:{message[0][0]}",
                f"time:{message[0][1]}",
                f"status:{message[0][2]}"
            ]
        return '\n'.join(w)
    else:
        return ''


class CryptoChat(discord.Client):
    PREFIX = "!"
    BOT = commands.Bot(command_prefix=PREFIX)

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
    async def connection_check(ctx) -> None:
        # await ctx.channel.send("")
        print(ctx.command)
        server = LocalDBMethods(db_addr())
        server.set_wal()

        embeded = discord.Embed(
            title="Crypto TradeBot Connection Report",
            description="Module Connection Info",
            color=0xFFFF00,
            timestamp=ctx.message.created_at
        )

        for module in clienttree.MODULES['middle']:
            cond1_normal = f'module = "{module}" and status = "normal"'
            cond1_error = f'module = "{module}" and status = "error"'
            cond2 = 'ORDER BY date, time DESC LIMIT 1'  # Choose recent 1
            r_n = server.select_db(
                target_table=table.TABLENAME_CLIENT,
                target_column=['date', 'time', 'status'],
                condition1=cond1_normal,
                condition2=cond2
            )
            r_e = server.select_db(
                target_table=table.TABLENAME_CLIENT,
                target_column=['date', 'time', 'status'],
                condition1=cond1_error,
                condition2=cond2
            )
            contents = '\n\n'.join([process_msg(r_n, normal=True),
                                    process_msg(r_e, normal=False)])
            embeded.add_field(
                name=clienttree.MODULES['middle'][module],
                value=contents,
                inline=True
            )
        await ctx.channel.send(embed=embeded)


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
