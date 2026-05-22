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
        print(f"✅ {len(synced)} commandes sync")
    except Exception as e:
        print(e)

# =========================
# RESET (SALONS + RÔLES SAFE)
# =========================
@bot.tree.command(name="reset", description="Reset complet du serveur (safe)")
async def reset(interaction: discord.Interaction):

    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message(
            "❌ Permission refusée.",
            ephemeral=True
        )

    await interaction.response.send_message(
        "🗑 Reset en cours...",
        ephemeral=True
    )

    guild = interaction.guild

    # 🔴 SUPPRIMER SALONS
    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass

    # 🔴 SUPPRIMER RÔLES (SAFE)
    for role in guild.roles:
        try:
            if role.name == "@everyone":
                continue
            if role.managed:  # bots / intégrations
                continue
            if role.position >= guild.me.top_role.position:
                continue

            await role.delete()
        except:
            pass

# =========================
# SETUP SERVER PRO
# =========================
@bot.tree.command(name="setup", description="Crée un serveur propre automatiquement")
async def setup(interaction: discord.Interaction):

    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message(
            "❌ Permission refusée.",
            ephemeral=True
        )

    guild = interaction.guild

    await interaction.response.send_message(
        "⚡ Création du serveur...",
        ephemeral=True
    )

    # =========================
    # RÔLES
    # =========================
    roles = [
        "👑 Owner",
        "🧠 Developer",
        "🛡 Admin",
        "🔧 Support",
        "💎 Premium",
        "🛒 Customer",
        "🧪 Beta Tester",
        "👤 Member",
        "✅ Verified"
    ]

    for role_name in roles:
        if not discord.utils.get(guild.roles, name=role_name):
            try:
                await guild.create_role(name=role_name)
            except:
                pass

    # =========================
    # CATÉGORIES
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
    # VOCAUX
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
