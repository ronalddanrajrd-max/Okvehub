import os
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot online: {bot.user}")
    await bot.tree.sync()

async def load():
    await bot.load_extension("cogs.shop")
    await bot.load_extension("cogs.tickets")
    await bot.load_extension("cogs.payments")
    await bot.load_extension("cogs.admin")

import asyncio

async def main():
    async with bot:
        await load()
        await bot.start(os.getenv("TOKEN"))

asyncio.run(main())
