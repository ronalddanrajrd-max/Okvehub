import discord
from discord.ext import commands

class Payments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="verify-roblox")
    async def verify(self, interaction: discord.Interaction, username: str):

        await interaction.response.send_message(
            f"🔎 Checking {username}",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Payments(bot))
