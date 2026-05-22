import discord
from discord.ext import commands
from config import ANNOUNCE_CHANNEL_ID, LOG_CHANNEL_ID

async def log(guild, message):
    channel = guild.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(message)

class Announcements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_admin(self, interaction):
        return interaction.user.guild_permissions.administrator

    @discord.app_commands.command(name="announce", description="Envoyer une annonce stylée")
    async def announce(
        self,
        interaction: discord.Interaction,
        title: str,
        message: str
    ):
        if not self.is_admin(interaction):
            return await interaction.response.send_message(
                "❌ Admin only.",
                ephemeral=True
            )

        channel = interaction.guild.get_channel(ANNOUNCE_CHANNEL_ID)

        if channel is None:
            return await interaction.response.send_message(
                "❌ Salon annonce introuvable. Vérifie ANNOUNCE_CHANNEL_ID dans config.py.",
                ephemeral=True
            )

        embed = discord.Embed(
            title=f"📢 {title}",
            description=(
                "```ansi\n"
                "\u001b[1;35m╔══════════════════════╗\u001b[0m\n"
                "\u001b[1;36m       OKVEHUB NEWS     \u001b[0m\n"
                "\u001b[1;35m╚══════════════════════╝\u001b[0m\n"
                "```\n"
                f"{message}"
            ),
            color=0x9b59b6
        )

        embed.set_footer(text=f"OkveHUB Announcement • {interaction.user}")
        embed.timestamp = discord.utils.utcnow()

        await channel.send("@everyone", embed=embed)

        await log(
            interaction.guild,
            f"📢 Annonce envoyée par {interaction.user.mention}"
        )

        await interaction.response.send_message(
            f"✅ Annonce envoyée dans {channel.mention}",
            ephemeral=True
        )

    @discord.app_commands.command(name="soon", description="Annonce automatique OkveHUB Soon")
    async def soon(self, interaction: discord.Interaction):
        if not self.is_admin(interaction):
            return await interaction.response.send_message(
                "❌ Admin only.",
                ephemeral=True
            )

        channel = interaction.guild.get_channel(ANNOUNCE_CHANNEL_ID)

        if channel is None:
            return await interaction.response.send_message(
                "❌ Salon annonce introuvable. Vérifie ANNOUNCE_CHANNEL_ID.",
                ephemeral=True
            )

        embed = discord.Embed(
            title="🚀 OKVEHUB IS COMING SOON...",
            description=(
                "🔥 Le projet avance très vite.\n\n"
                "💎 Script premium\n"
                "⚡ Système automatique\n"
                "🔐 Sécurité renforcée\n"
                "📦 Livraison instantanée\n"
                "🎮 Roblox ready\n\n"
                "**Restez connectés. Le vrai niveau arrive.**"
            ),
            color=0xff00ff
        )

        embed.set_footer(text="OkveHUB • Soon")
        embed.timestamp = discord.utils.utcnow()

        await channel.send("@everyone", embed=embed)

        await log(
            interaction.guild,
            f"🚀 Annonce Soon envoyée par {interaction.user.mention}"
        )

        await interaction.response.send_message(
            "✅ Annonce Soon envoyée.",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Announcements(bot))
