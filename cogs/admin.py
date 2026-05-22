import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="add-brainrot")
    async def add(self, interaction: discord.Interaction, user: discord.Member, amount: int):

        await interaction.response.send_message(
            f"🧠 +{amount} brainrot for {user}",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Admin(bot))
