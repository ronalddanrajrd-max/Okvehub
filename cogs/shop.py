import discord
from discord.ext import commands

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="shop")
    async def shop(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            "🛒 Shop panel (OK)",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Shop(bot))
