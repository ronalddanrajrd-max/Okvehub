import discord
from discord.ext import commands
import asyncio
import requests
from database import load, save
from config import LTC_ADDRESS, CUSTOMER_ROLE_NAME, LOG_CHANNEL_NAME

PRODUCT_NAME = "OkveHUB Premium"
PRODUCT_LINK = "TON SCRIPT OU TON LIEN ICI"
BRAINROT_PRICE = 1

def ltc_balance(address):
    url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance"
    r = requests.get(url, timeout=10)
    return r.json().get("balance", 0)

async def send_log(guild, text):
    channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
    if channel:
        await channel.send(text)

async def give_customer(user, guild):
    role = discord.utils.get(guild.roles, name=CUSTOMER_ROLE_NAME)
    if role:
        await user.add_roles(role)

async def deliver(user):
    try:
        await user.send(
            f"✅ **OKVEHUB DELIVERY**\n\n"
            f"Produit : `{PRODUCT_NAME}`\n\n"
            f"📦 Ton accès :\n"
            f"`{PRODUCT_LINK}`"
        )
    except:
        pass

class ShopView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="💰 Litecoin", style=discord.ButtonStyle.green)
    async def ltc(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not LTC_ADDRESS:
            return await interaction.response.send_message(
                "❌ LTC_ADDRESS n'est pas configuré sur Railway.",
                ephemeral=True
            )

        embed = discord.Embed(
            title="💰 OKVEHUB LTC PAYMENT",
            description=(
                "🔐 Création d'une commande sécurisée...\n\n"
                "Merci de patienter."
            ),
            color=0x00ff99
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)
        msg = await interaction.original_response()

        steps = [
            "🔄 Connexion à la blockchain Litecoin...",
            "🧾 Génération de la commande...",
            "💰 En attente du paiement...",
            "⏳ Vérification des confirmations...",
        ]

        for step in steps:
            embed.description = step + "\n\n`████▒▒▒▒▒▒`"
            await msg.edit(embed=embed)
            await asyncio.sleep(1)

        embed.description = (
            "💰 **Envoie ton paiement LTC ici :**\n\n"
            f"`{LTC_ADDRESS}`\n\n"
            "Après avoir payé, clique sur **Check Payment**."
        )
        embed.set_footer(text="OkveHUB Secure Payment System")
        await msg.edit(embed=embed, view=LTCCheckView())

    @discord.ui.button(label="🎮 Robux", style=discord.ButtonStyle.blurple)
    async def robux(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🎮 OKVEHUB ROBUX PAYMENT",
            description=(
                "1️⃣ Achète le gamepass\n"
                "2️⃣ Fais la commande :\n"
                "`/verify-robux username gamepass_id`\n\n"
                "✅ Si l'achat est détecté : rôle + DM automatique."
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
                f"❌ Tu n'as pas assez de Brainrot.\nBalance : `{balance}`",
                ephemeral=True
            )

        data["brainrot"][uid] -= BRAINROT_PRICE
        data["orders"].append({
            "user": str(interaction.user),
            "user_id": uid,
            "product": PRODUCT_NAME,
            "payment": "Brainrot",
            "status": "paid"
        })
        save(data)

        await give_customer(interaction.user, interaction.guild)
        await deliver(interaction.user)
        await send_log(interaction.guild, f"🧪 Achat Brainrot validé : {interaction.user.mention}")

        await interaction.response.send_message(
            "✅ Paiement Brainrot validé. Produit envoyé en DM.",
            ephemeral=True
        )

class LTCCheckView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="🔄 Check Payment", style=discord.ButtonStyle.green)
    async def check(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        embed = discord.Embed(
            title="🔄 LTC CHECKING",
            description="Connexion à l’API blockchain...",
            color=0xffcc00
        )

        msg = await interaction.followup.send(embed=embed, ephemeral=True)

        loading = [
            "🔍 Scan blockchain `▰▱▱▱▱`",
            "🔍 Scan blockchain `▰▰▱▱▱`",
            "🔍 Scan blockchain `▰▰▰▱▱`",
            "🔍 Scan blockchain `▰▰▰▰▱`",
            "🔍 Scan blockchain `▰▰▰▰▰`",
        ]

        for text in loading:
            embed.description = text
            await msg.edit(embed=embed)
            await asyncio.sleep(1)

        try:
            balance = ltc_balance(LTC_ADDRESS)
        except Exception as e:
            embed.title = "❌ API ERROR"
            embed.description = f"Erreur : `{e}`"
            embed.color = 0xff0000
            return await msg.edit(embed=embed)

        if balance <= 0:
            embed.title = "❌ PAYMENT NOT FOUND"
            embed.description = (
                "Aucun paiement détecté pour l’instant.\n\n"
                "Attends quelques secondes puis reclique sur **Check Payment**."
            )
            embed.color = 0xff0000
            return await msg.edit(embed=embed)

        data = load()
        data["orders"].append({
            "user": str(interaction.user),
            "user_id": str(interaction.user.id),
            "product": PRODUCT_NAME,
            "payment": "LTC",
            "status": "paid"
        })
        save(data)

        await give_customer(interaction.user, interaction.guild)
        await deliver(interaction.user)
        await send_log(interaction.guild, f"💰 LTC validé pour {interaction.user.mention}")

        embed.title = "✅ PAYMENT CONFIRMED"
        embed.description = (
            "Paiement détecté.\n\n"
            "📦 Produit envoyé en DM.\n"
            "🎖 Rôle Customer ajouté."
        )
        embed.color = 0x00ff00
        await msg.edit(embed=embed)

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="shop", description="Afficher le shop OkveHUB")
    async def shop(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="💎 OKVEHUB PREMIUM SHOP",
            description=(
                "```ansi\n"
                "[1;36m╔══════════════════════╗[0m\n"
                "[1;35m      OKVEHUB PRO      [0m\n"
                "[1;36m╚══════════════════════╝[0m\n"
                "```\n"
                "🔥 **Script premium bientôt disponible**\n"
                "⚡ Livraison automatique\n"
                "🔐 Paiement sécurisé\n"
                "🎖 Rôle Customer automatique\n\n"
                "**Méthodes disponibles :**\n"
                "💰 Litecoin\n"
                "🎮 Robux\n"
                "🧪 Brainrot"
            ),
            color=0x9b59b6
        )

        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/5968/5968756.png")
        embed.set_footer(text="OkveHUB • Automated Premium System")

        await interaction.channel.send(embed=embed, view=ShopView())
        await interaction.response.send_message("✅ Panel shop PRO envoyé.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Shop(bot))
