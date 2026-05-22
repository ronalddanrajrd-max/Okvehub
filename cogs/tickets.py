import discord
from discord.ext import commands

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ticket-panel")
    async def ticket(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            "🎫 Ticket system ready",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Tickets(bot))
