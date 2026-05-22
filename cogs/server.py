import discord
from discord.ext import commands
from config import AUTO_ROLE_ID, WELCOME_CHANNEL_ID, LOG_CHANNEL_ID

async def send_log(guild, message):
    channel = guild.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(message)

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        role = member.guild.get_role(AUTO_ROLE_ID)

        if role:
            try:
                await member.add_roles(role)
            except:
                pass

        welcome = member.guild.get_channel(WELCOME_CHANNEL_ID)

        if welcome:
            embed = discord.Embed(
                title="👋 Welcome to OkveHUB",
                description=(
                    f"Bienvenue {member.mention} !\n\n"
                    "💎 Découvre OkveHUB\n"
                    "🛒 Va voir le shop\n"
                    "🎫 Ouvre un ticket si besoin"
                ),
                color=0x00ff99
            )

            embed.set_thumbnail(url=member.display_avatar.url)

            await welcome.send(embed=embed)

        await send_log(
            member.guild,
            f"✅ Nouveau membre : {member.mention}"
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await send_log(
            member.guild,
            f"❌ Membre parti : `{member}`"
        )

    @discord.app_commands.command(name="server-info", description="Infos serveur")
    async def server_info(self, interaction: discord.Interaction):
        guild = interaction.guild

        embed = discord.Embed(
            title="📊 SERVER INFO",
            description=(
                f"🏷 Nom : `{guild.name}`\n"
                f"👥 Membres : `{guild.member_count}`\n"
                f"📁 Salons : `{len(guild.channels)}`\n"
                f"🎭 Rôles : `{len(guild.roles)}`"
            ),
            color=0x5865F2
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Server(bot))
