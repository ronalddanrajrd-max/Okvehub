import os
import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# READY
# =========================
@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} commandes synchronisées")
    except Exception as e:
        print(e)

# =========================
# RESET (SUPPRIME TOUT)
# =========================
@bot.tree.command(name="reset", description="Supprime tous les salons et catégories")
async def reset(interaction: discord.Interaction):

    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message(
            "❌ Tu n'as pas la permission.",
            ephemeral=True
        )

    await interaction.response.send_message(
        "🗑 Suppression du serveur en cours...",
        ephemeral=True
    )

    for channel in interaction.guild.channels:
        try:
            await channel.delete()
        except:
            pass

# =========================
# SETUP SERVER PRO
# =========================
@bot.tree.command(name="setup", description="Crée un serveur propre automatiquement")
async def setup(interaction: discord.Interaction):

    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message(
            "❌ Tu n'as pas la permission.",
            ephemeral=True
        )

    guild = interaction.guild

    await interaction.response.send_message(
        "⚡ Création du serveur en cours...",
        ephemeral=True
    )

    # =========================
    # ROLES
    # =========================
    roles = [
        "👑 Owner",
        "🧠 Developer",
        "🛡 Admin",
        "🔧 Support",
        "💎 Premium",
        "🛒 Customer",
        "🧪 Beta Tester",
        "✅ Verified",
        "👤 Member"
    ]

    for role in roles:
        if not discord.utils.get(guild.roles, name=role):
            await guild.create_role(name=role)

    # =========================
    # CATEGORIES
    # =========================
    info = await guild.create_category("📌・INFORMATIONS")
    store = await guild.create_category("🛒・STORE")
    support = await guild.create_category("🎫・SUPPORT")
    community = await guild.create_category("💬・COMMUNITY")
    voice = await guild.create_category("🔊・VOICE")

    # =========================
    # INFORMATIONS
    # =========================
    await guild.create_text_channel("👋・welcome", category=info)
    await guild.create_text_channel("📜・rules", category=info)
    await guild.create_text_channel("📢・announcements", category=info)
    await guild.create_text_channel("📡・status", category=info)

    # =========================
    # STORE
    # =========================
    await guild.create_text_channel("🛒・buy", category=store)
    await guild.create_text_channel("💸・prices", category=store)
    await guild.create_text_channel("🎥・showcase", category=store)
    await guild.create_text_channel("📝・changelogs", category=store)

    # =========================
    # SUPPORT
    # =========================
    await guild.create_text_channel("🎫・create-ticket", category=support)
    await guild.create_text_channel("❓・faq", category=support)
    await guild.create_text_channel("🐞・bug-report", category=support)

    # =========================
    # COMMUNITY
    # =========================
    await guild.create_text_channel("💬・general", category=community)
    await guild.create_text_channel("💻・scripts-chat", category=community)
    await guild.create_text_channel("📸・media", category=community)

    # =========================
    # VOICE
    # =========================
    await guild.create_voice_channel("💬 General", category=voice)
    await guild.create_voice_channel("💻 Coding", category=voice)
    await guild.create_voice_channel("🛠 Support", category=voice)
    await guild.create_voice_channel("🎵 Chill", category=voice)

    await interaction.followup.send(
        "✅ Serveur créé avec succès !",
        ephemeral=True
    )

# =========================
# RUN BOT
# =========================
bot.run(os.getenv("TOKEN"))
