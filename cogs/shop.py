import discord
from discord.ext import commands
import asyncio
import requests
from database import load, save
from config import (
    LTC_ADDRESS,
    CUSTOMER_ROLE_ID,
    LOG_CHANNEL_ID,
    PRODUCT_NAME,
    PRODUCT_LINK,
    BRAINROT_PRICE
)

def ltc_balance(address):
    url = f"https://litecoinspace.org/api/address/{address}"

    r = requests.get(url, timeout=15)

    if r.status_code != 200:
        raise Exception(f"API LTC error {r.status_code}")

    data = r.json()

    funded = data["chain_stats"]["funded_txo_sum"] + data["mempool_stats"]["funded_txo_sum"]
    spent = data["chain_stats"]["spent_txo_sum"] + data["mempool_stats"]["spent_txo_sum"]

    return funded - spent

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

class LTCCheckView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="🔄 Check Payment", style=discord.ButtonStyle.green)
    async def check_payment(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        embed = discord.Embed(
            title="🔄 LTC PAYMENT CHECK",
            description="Connexion à la blockchain...",
            color=0xffcc00
        )

        msg = await interaction.followup.send(embed=embed, ephemeral=True)

        steps = [
            "🔍 Scan blockchain `▰▱▱▱▱`",
            "🔍 Scan blockchain `▰▰▱▱▱`",
            "🔍 Scan blockchain `▰▰▰▱▱`",
            "🔍 Scan blockchain `▰▰▰▰▱`",
            "🔍 Scan blockchain `▰▰▰▰▰`"
        ]

        for step in steps:
            embed.description = step
            await msg.edit(embed=embed)
            await asyncio.sleep(1)

        try:
            balance = ltc_balance(LTC_ADDRESS)
        except Exception as e:
            embed.title = "❌ LTC API ERROR"
            embed.description = f"Erreur : `{e}`"
            embed.color = 0xff0000
            return await msg.edit(embed=embed)

        if balance <= 0:
            embed.title = "❌ PAYMENT NOT FOUND"
            embed.description = "Aucun paiement LTC détecté pour l’instant."
            embed.color = 0xff0000
            return await msg.edit(embed=embed)

        await give_customer(interaction.user)
        await deliver(interaction.user)

        data = load()
        data["orders"].append({
            "user": str(interaction.user),
            "user_id": str(interaction.user.id),
            "payment": "LTC",
            "product": PRODUCT_NAME,
            "status": "paid"
        })
        save(data)

        await log(interaction.guild, f"💰 LTC validé pour {interaction.user.mention}")

        embed.title = "✅ PAYMENT CONFIRMED"
        embed.description = "Paiement LTC détecté.\n\n📦 Produit envoyé en DM.\n🎖 Rôle Customer ajouté."
        embed.color = 0x00ff00
        await msg.edit(embed=embed)

class ShopView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="💰 Litecoin", style=discord.ButtonStyle.green)
    async def ltc(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="💰 OKVEHUB LTC PAYMENT",
            description="🔐 Création de la commande sécurisée...",
            color=0x00ff99
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)
        msg = await interaction.original_response()

        steps = [
            "🔄 Connexion blockchain...",
            "🧾 Génération commande...",
            "💰 Préparation adresse LTC...",
            "✅ Commande prête."
        ]

        for step in steps:
            embed.description = step + "\n\n`▰▰▰▱▱`"
            await msg.edit(embed=embed)
            await asyncio.sleep(1)

        embed.description = (
            "💰 **Adresse LTC :**\n"
            f"`{LTC_ADDRESS}`\n\n"
            "Après paiement, clique sur **Check Payment**."
        )

        await msg.edit(embed=embed, view=LTCCheckView())

    @discord.ui.button(label="🎮 Robux", style=discord.ButtonStyle.blurple)
    async def robux(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🎮 OKVEHUB ROBUX PAYMENT",
            description=(
                "Après achat du gamepass :\n\n"
                "`/verify-robux username gamepass_id`\n\n"
                "Le bot vérifie automatiquement Roblox."
            ),
            color=0x5865F2
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="🧪 Brainrot", style=discord.ButtonStyle.red)
    async def brainrot(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = load()
        uid = str(interaction.user.id)

        balance = data["brainrot"].get(uid, 0)

        if balance < BRAINROT_PRICE:
            return await interaction.response.send_message(
                f"❌ Balance insuffisante : `{balance}` Brainrot",
                ephemeral=True
            )

        data["brainrot"][uid] -= BRAINROT_PRICE
        data["orders"].append({
            "user": str(interaction.user),
            "user_id": uid,
            "payment": "Brainrot",
            "product": PRODUCT_NAME,
            "status": "paid"
        })
        save(data)

        await give_customer(interaction.user)
        await deliver(interaction.user)

        await log(interaction.guild, f"🧪 Brainrot validé pour {interaction.user.mention}")

        await interaction.response.send_message(
            "✅ Paiement Brainrot validé. Produit envoyé en DM.",
            ephemeral=True
        )

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="shop", description="Envoyer le panel shop")
    async def shop(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="💎 OKVEHUB PREMIUM SHOP",
            description=(
                "🔥 **OkveHUB Premium**\n\n"
                "⚡ Livraison automatique\n"
                "🔐 Paiement sécurisé\n"
                "🎖 Rôle Customer automatique\n\n"
                "💰 Litecoin\n"
                "🎮 Robux\n"
                "🧪 Brainrot"
            ),
            color=0x9b59b6
        )

        embed.set_footer(text="OkveHUB Automated Shop")

        await interaction.response.send_message("✅ Panel envoyé.", ephemeral=True)
        await interaction.channel.send(embed=embed, view=ShopView())

async def setup(bot):
    await bot.add_cog(Shop(bot))
