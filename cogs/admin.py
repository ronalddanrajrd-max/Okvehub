import discord
from discord.ext import commands
from database import load, save

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="add-brainrot",
        description="Add brainrot"
    )
    async def add(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        amount: int
    ):

        data = load()

        uid = str(user.id)

        data["brainrot"][uid] = (
            data["brainrot"].get(uid, 0)
            + amount
        )

        save(data)

        await interaction.response.send_message(
            f"✅ Added {amount} brainrot to {user}",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Admin(bot))
