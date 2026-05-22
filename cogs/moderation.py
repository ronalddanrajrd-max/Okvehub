import discord
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="clear",
        description="Delete messages"
    )
    async def clear(
        self,
        interaction: discord.Interaction,
        amount: int
    ):

        await interaction.channel.purge(limit=amount)

        await interaction.response.send_message(
            f"✅ Deleted {amount} messages",
            ephemeral=True
        )

    @discord.app_commands.command(
        name="kick",
        description="Kick member"
    )
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason"
    ):

        await member.kick(reason=reason)

        await interaction.response.send_message(
            f"✅ {member} kicked"
        )

    @discord.app_commands.command(
        name="ban",
        description="Ban member"
    )
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason"
    ):

        await member.ban(reason=reason)

        await interaction.response.send_message(
            f"✅ {member} banned"
        )

async def setup(bot):
    await bot.add_cog(Moderation(bot))
