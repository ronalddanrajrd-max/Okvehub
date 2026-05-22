import os
import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commandes synchronisées")
    except Exception as e:
        print(e)

# COMMANDE SETUP
@bot.tree.command(
    name="setup",
    description="Configure automatiquement le serveur"
)
async def setup(interaction: discord.Interaction):

    guild = interaction.guild

    # ROLES
    roles = [
        "Owner",
        "Developer",
        "Admin",
        "Support",
        "Customer",
        "Premium",
        "Beta Tester",
        "Member",
        "Verified"
    ]

    for role_name in roles:
        if not discord.utils.get(guild.roles, name=role_name):
            await guild.create_role(name=role_name)

    # CATEGORIES
    info_category = await guild.create_category("📌 INFORMATIONS")
    store_category = await guild.create_category("🛒 STORE")
    support_category = await guild.create_category("🎫 SUPPORT")
    community_category = await guild.create_category("💬 COMMUNITY")
    voice_category = await guild.create_category("🔊 VOICE")

    # SALONS INFORMATIONS
    await guild.create_text_channel("welcome", category=info_category)
    await guild.create_text_channel("rules", category=info_category)
    await guild.create_text_channel("announcements", category=info_category)
    await guild.create_text_channel("status", category=info_category)

    # STORE
    await guild.create_text_channel("buy", category=store_category)
    await guild.create_text_channel("prices", category=store_category)
    await guild.create_text_channel("showcase", category=store_category)
    await guild.create_text_channel("changelogs", category=store_category)

    # SUPPORT
    await guild.create_text_channel("create-ticket", category=support_category)
    await guild.create_text_channel("faq", category=support_category)
    await guild.create_text_channel("bug-report", category=support_category)

    # COMMUNITY
    await guild.create_text_channel("general", category=community_category)
    await guild.create_text_channel("scripts-chat", category=community_category)
    await guild.create_text_channel("media", category=community_category)

    # VOCAUX
    await guild.create_voice_channel("General", category=voice_category)
    await guild.create_voice_channel("Coding", category=voice_category)
    await guild.create_voice_channel("Support Voice", category=voice_category)
    await guild.create_voice_channel("Chill", category=voice_category)

    await interaction.response.send_message(
        "✅ Serveur configuré avec succès.",
        ephemeral=True
    )

bot.run(os.getenv("TOKEN"))
