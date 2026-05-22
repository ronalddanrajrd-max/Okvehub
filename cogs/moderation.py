import discord
from discord.ext import commands
import datetime
from config import LOG_CHANNEL_ID

async def send_log(guild, message):
    channel = guild.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(message)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="clear", description="Supprimer des messages")
    async def clear(self, interaction: discord.Interaction, amount: int):
        if not interaction.user.guild_permissions.manage_messages:
            return await interaction.response.send_message("❌ Permission refusée.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)

        deleted = await interaction.channel.purge(limit=amount)

        await send_log(
            interaction.guild,
            f"🧹 {len(deleted)} messages supprimés par {interaction.user.mention}"
        )

        await interaction.followup.send(
            f"✅ `{len(deleted)}` messages supprimés.",
            ephemeral=True
        )

    @discord.app_commands.command(name="kick", description="Kick un membre")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison"):
        if not interaction.user.guild_permissions.kick_members:
            return await interaction.response.send_message("❌ Permission refusée.", ephemeral=True)

        await member.kick(reason=reason)

        await send_log(
            interaction.guild,
            f"👢 {member.mention} kick par {interaction.user.mention} | `{reason}`"
        )

        await interaction.response.send_message(f"✅ {member.mention} expulsé.")

    @discord.app_commands.command(name="ban", description="Ban un membre")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison"):
        if not interaction.user.guild_permissions.ban_members:
            return await interaction.response.send_message("❌ Permission refusée.", ephemeral=True)

        await member.ban(reason=reason)

        await send_log(
            interaction.guild,
            f"🔨 {member.mention} ban par {interaction.user.mention} | `{reason}`"
        )

        await interaction.response.send_message(f"✅ {member.mention} banni.")

    @discord.app_commands.command(name="mute", description="Mute un membre")
    async def mute(self, interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "Aucune raison"):
        if not interaction.user.guild_permissions.moderate_members:
            return await interaction.response.send_message("❌ Permission refusée.", ephemeral=True)

        until = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
        await member.timeout(until, reason=reason)

        await send_log(
            interaction.guild,
            f"🔇 {member.mention} mute {minutes}min par {interaction.user.mention}"
        )

        await interaction.response.send_message(
            f"✅ {member.mention} mute `{minutes}` minutes."
        )

    @discord.app_commands.command(name="unmute", description="Unmute un membre")
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        if not interaction.user.guild_permissions.moderate_members:
            return await interaction.response.send_message("❌ Permission refusée.", ephemeral=True)

        await member.timeout(None)

        await send_log(
            interaction.guild,
            f"🔊 {member.mention} unmute par {interaction.user.mention}"
        )

        await interaction.response.send_message(f"✅ {member.mention} unmute.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
