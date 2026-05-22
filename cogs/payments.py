import discord
from discord.ext import commands
import requests
import asyncio
from database import load, save
from config import (
    CUSTOMER_ROLE_ID,
    LOG_CHANNEL_ID,
    PRODUCT_NAME,
    PRODUCT_LINK
)

async def log(guild, message):
    channel = guild.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(message)

async def give_customer(member):
    role = member.guild.get_role(CUSTOMER_ROLE_ID)
    if role:
        await member.add_roles(role)

async def deliver(user):
    try:
        await user.send(
            f"✅ **OKVEHUB DELIVERY**\n\n"
            f"Produit : `{PRODUCT_NAME}`\n\n"
            f"📦 Accès :\n`{PRODUCT_LINK}`"
        )
    except:
        pass

def roblox_user_id(username):
    r = requests.post(
        "https://users.roblox.com/v1/usernames/users",
        json={"usernames": [username]},
        timeout=15
    )

    data = r.json()

    if not data.get("data"):
        return None

    return data["data"][0]["id"]

def owns_gamepass(user_id, gamepass_id):
    r = requests.get(
        f"https://inventory.roblox.com/v1/users/{user_id}/items/GamePass/{gamepass_id}",
        timeout=15
    )

    data = r.json()
    return len(data.get("data", [])) > 0

class Payments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="verify-robux", description="Vérifier un achat Robux Gamepass")
    async def verify_robux(
        self,
        interaction: discord.Interaction,
        username: str,
        gamepass_id: int
    ):
        await interaction.response.defer(ephemeral=True)

        embed = discord.Embed(
            title="🎮 OKVEHUB ROBUX CHECK",
            description="Connexion à Roblox API...",
            color=0x5865F2
        )

        msg = await interaction.followup.send(embed=embed, ephemeral=True)

        steps = [
            "🔎 Recherche du joueur Roblox...",
            "🎮 Vérification du gamepass...",
            "🔐 Validation de l'achat...",
            "📦 Préparation de la livraison..."
        ]

        for step in steps:
            embed.description = step + "\n\n`▰▰▱▱▱`"
            await msg.edit(embed=embed)
            await asyncio.sleep(1)

        try:
            user_id = roblox_user_id(username)

            if user_id is None:
                embed.title = "❌ ROBLOX USER NOT FOUND"
                embed.description = "Le pseudo Roblox est introuvable."
                embed.color = 0xff0000
                return await msg.edit(embed=embed)

            if not owns_gamepass(user_id, gamepass_id):
                embed.title = "❌ GAMEPASS NOT FOUND"
                embed.description = "Le gamepass n'a pas été détecté sur ce compte."
                embed.color = 0xff0000
                return await msg.edit(embed=embed)

        except Exception as e:
            embed.title = "❌ ROBLOX API ERROR"
            embed.description = f"Erreur : `{e}`"
            embed.color = 0xff0000
            return await msg.edit(embed=embed)

        await give_customer(interaction.user)
        await deliver(interaction.user)

        data = load()
        data["orders"].append({
            "user": str(interaction.user),
            "user_id": str(interaction.user.id),
            "roblox_username": username,
            "gamepass_id": gamepass_id,
            "payment": "Robux",
            "product": PRODUCT_NAME,
            "status": "paid"
        })
        save(data)

        await log(
            interaction.guild,
            f"🎮 Robux validé pour {interaction.user.mention} | Roblox: `{username}`"
        )

        embed.title = "✅ ROBUX PAYMENT CONFIRMED"
        embed.description = (
            "Achat validé.\n\n"
            "📦 Produit envoyé en DM.\n"
            "🎖 Rôle Customer ajouté."
        )
        embed.color = 0x00ff00

        await msg.edit(embed=embed)

async def setup(bot):
    await bot.add_cog(Payments(bot))
