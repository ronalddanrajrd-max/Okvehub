
import discord
from discord.ext import commands
from config import ANNOUNCE_CHANNEL_NAME, LOG_CHANNEL_NAME

async def log(guild, message):
    channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
    if channel:
        await channel.send(message)

class Announcements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_admin(self, interaction):
        return interaction.user.guild_permissions.administrator

    @discord.app_commands.command(name="announce", description="Envoyer une annonce automatique")
    async def announce(
        self,
        interaction: discord.Interaction,
        title: str,
        message: str
    ):
        if not self.is_admin(interaction):
            return await interaction.response.send_message("❌ Admin only.", ephemeral=True)

        channel = discord.utils.get(interaction.guild.text_channels, name=ANNOUNCE_CHANNEL_NAME)

        if channel is None:
            channel = await interaction.guild.create_text_channel(ANNOUNCE_CHANNEL_NAME)

        embed = discord.Embed(
            title=f"📢 {title}",
            description=message,
            color=0xffcc00
        )

        embed.set_footer(text=f"Annonce par {interaction.user}")

        await channel.send("@everyone", embed=embed)

        await log(interaction.guild, f"📢 Annonce envoyée par {interaction.user.mention}")

        await interaction.response.send_message(
            f"✅ Annonce envoyée dans {channel.mention}",
            ephemeral=True
        )

    @discord.app_commands.command(name="auto-setup", description="Créer les salons importants automatiquement")
    async def auto_setup(self, interaction: discord.Interaction):
        if not self.is_admin(interaction):
            return await interaction.response.send_message("❌ Admin only.", ephemeral=True)

        guild = interaction.guild

        needed_channels = [
            ANNOUNCE_CHANNEL_NAME,
            LOG_CHANNEL_NAME,
            "shop",
            "support"
        ]

        created = []

        for name in needed_channels:
            channel = discord.utils.get(guild.text_channels, name=name)

            if channel is None:
                await guild.create_text_channel(name)
                created.append(name)

        role = discord.utils.get(guild.roles, name="Customer")

        if role is None:
            await guild.create_role(name="Customer")
            created.append("role Customer")

        await interaction.response.send_message(
            "✅ Auto setup terminé.\nCréé : " + ", ".join(created) if created else "✅ Tout existe déjà.",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Announcements(bot))
