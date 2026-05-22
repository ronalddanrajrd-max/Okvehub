import discord
from discord.ext import commands
import asyncio
from config import TOKEN

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

COGS = [
    "cogs.shop",
    "cogs.tickets",
    "cogs.payments",
    "cogs.admin",
    "cogs.moderation",
    "cogs.announcements",
    "cogs.server"
]

@bot.event
async def on_ready():
    print(f"✅ Bot connecté : {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Commandes synchronisées : {len(synced)}")
    except Exception as e:
        print(f"❌ Erreur sync : {e}")

async def load_cogs():
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"✅ Cog chargé : {cog}")
        except Exception as e:
            print(f"❌ Erreur cog {cog}: {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())
