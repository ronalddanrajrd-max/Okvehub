import os
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"✅ Connected as {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} commands")
    except Exception as e:
        print(e)

async def load_cogs():

    await bot.load_extension("cogs.shop")
    await bot.load_extension("cogs.tickets")
    await bot.load_extension("cogs.payments")
    await bot.load_extension("cogs.moderation")
    await bot.load_extension("cogs.admin")

async def main():

    async with bot:
        await load_cogs()
        await bot.start(os.getenv("TOKEN"))

asyncio.run(main())
