import discord
from discord.ext import commands
from config import LOG_CHANNEL_NAME

async def log(guild, message):
    channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
    if channel:
        await channel.send(message)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def can_moderate(self, interaction):
        return interaction.user.guild_permissions.manage_messages

    @discord.app_commands.command(name="clear", description="Supprimer des messages")
    async def clear(self, interaction: discord.Interaction, amount: int):
        if not self.can_moderate(interaction):
            return await interaction.response.send_message("❌ Permission refusée.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)

        deleted = await interaction.channel.purge(limit=amount)

        await log(interaction.guild, f"🧹 {len(deleted)} messages supprimés par {interaction.user.mention}")

        await interaction.followup.send(f"✅ {len(deleted)} messages supprimés.")

    @discord.app_commands.command(name="kick", description="Expulser un membre")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison"):
        if not interaction.user.guild_permissions.kick_members:
            return await interaction.response.send_message("❌ Permission refusée.", ephemeral=True)

        await member.kick(reason=reason)

        await log(interaction.guild, f"👢 {member.mention} kick par {interaction.user.mention} | {reason}")

        await interaction.response.send_message(f"✅ {member.mention} expulsé.")

    @discord.app_commands.command(name="ban", description="Bannir un membre")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison"):
        if not interaction.user.guild_permissions.ban_members:
            return await interaction.response.send_message("❌ Permission refusée.", ephemeral=True)

        await member.ban(reason=reason)

        await log(interaction.guild, f"🔨 {member.mention} ban par {interaction.user.mention} | {reason}")

        await interaction.response.send_message(f"✅ {member.mention} banni.")

    @discord.app_commands.command(name="mute", description="Timeout un membre")
    async def mute(self, interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "Aucune raison"):
        if not interaction.user.guild_permissions.moderate_members:
            return await interaction.response.send_message("❌ Permission refusée.", ephemeral=True)

        import datetime

        until = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)

        await member.timeout(until, reason=reason)

        await log(interaction.guild, f"🔇 {member.mention} mute {minutes} min par {interaction.user.mention}")

        await interaction.response.send_message(f"✅ {member.mention} mute {minutes} minutes.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
