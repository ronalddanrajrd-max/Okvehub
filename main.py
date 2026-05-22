import discord
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Bot connecté : {bot.user}")

bot.run("TON_TOKEN")
