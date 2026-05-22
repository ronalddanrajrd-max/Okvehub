import os
import asyncio
import discord
from discord.ext import commands
from config import TOKEN

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

COGS = [
    "cogs.shop",
    "cogs.tickets",
    "cogs.payments",
    "cogs.admin",
    "cogs.moderation",
    "cogs.announcements"
]

@bot.event
async def on_ready():
    print(f"✅ Bot connecté : {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Slash commands sync : {len(synced)}")
    except Exception as e:
        print(f"❌ Sync error : {e}")

async def load_cogs():
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"✅ Loaded {cog}")
        except Exception as e:
            print(f"❌ Error loading {cog}: {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())
