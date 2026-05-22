import discord
from discord.ext import commands
from config import ANNOUNCE_CHANNEL_NAME, LOG_CHANNEL_NAME

async def log(guild, text):
    channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
    if channel:
        await channel.send(text)

class Announcements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def admin(self, interaction):
        return interaction.user.guild_permissions.administrator

    @discord.app_commands.command(name="announce", description="Envoyer une annonce stylée")
    async def announce(self, interaction: discord.Interaction, title: str, message: str):
        if not self.admin(interaction):
            return await interaction.response.send_message("❌ Admin only.", ephemeral=True)

        channel = discord.utils.get(interaction.guild.text_channels, name=ANNOUNCE_CHANNEL_NAME)

        if channel is None:
            channel = await interaction.guild.create_text_channel(ANNOUNCE_CHANNEL_NAME)

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

        await log(interaction.guild, f"📢 Annonce envoyée par {interaction.user.mention}")

        await interaction.response.send_message(
            f"✅ Annonce envoyée dans {channel.mention}",
            ephemeral=True
        )

    @discord.app_commands.command(name="soon", description="Annonce automatique OkveHUB Soon")
    async def soon(self, interaction: discord.Interaction):
        if not self.admin(interaction):
            return await interaction.response.send_message("❌ Admin only.", ephemeral=True)

        channel = discord.utils.get(interaction.guild.text_channels, name=ANNOUNCE_CHANNEL_NAME)

        if channel is None:
            channel = await interaction.guild.create_text_channel(ANNOUNCE_CHANNEL_NAME)

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

        await log(interaction.guild, f"🚀 Annonce Soon envoyée par {interaction.user.mention}")

        await interaction.response.send_message("✅ Annonce Soon envoyée.", ephemeral=True)

    @discord.app_commands.command(name="auto-setup", description="Créer salons + rôle automatiquement")
    async def auto_setup(self, interaction: discord.Interaction):
        if not self.admin(interaction):
            return await interaction.response.send_message("❌ Admin only.", ephemeral=True)

        guild = interaction.guild

        channels = [
            ANNOUNCE_CHANNEL_NAME,
            LOG_CHANNEL_NAME,
            "shop",
            "support",
            "rules"
        ]

        created = []

        for name in channels:
            if discord.utils.get(guild.text_channels, name=name) is None:
                await guild.create_text_channel(name)
                created.append(f"#{name}")

        if discord.utils.get(guild.roles, name="Customer") is None:
            await guild.create_role(name="Customer")
            created.append("Role Customer")

        embed = discord.Embed(
            title="✅ AUTO SETUP FINISHED",
            description="Créé :\n" + "\n".join(created) if created else "Tout existait déjà.",
            color=0x00ff99
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Announcements(bot))
