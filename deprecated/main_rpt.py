from discord.ext import commands
import discord
import asyncio
import os


_p = "!"
bot = commands.Bot(command_prefix=_p)


async def on_ready():
    game = discord.Game("comment")
    await bot.change_presence(status=discord.Status.online, activity=game)


