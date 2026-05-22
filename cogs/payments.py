import discord
from discord.ext import commands
import requests
from database import load, save
from config import LTC_ADDRESS, CUSTOMER_ROLE_NAME, LOG_CHANNEL_NAME

PRODUCT_NAME = "Premium Script"

async def log(guild, message):
    channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
    if channel:
        await channel.send(message)

def get_ltc_balance(address):
    url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance"
    r = requests.get(url, timeout=10)
    data = r.json()
    return data.get("balance", 0)

def username_to_id(username):
    r = requests.post(
        "https://users.roblox.com/v1/usernames/users",
        json={"usernames": [username]},
        timeout=10
    )
    data = r.json()

    if not data.get("data"):
        return None

    return data["data"][0]["id"]

def owns_gamepass(user_id, gamepass_id):
    url = f"https://inventory.roblox.com/v1/users/{user_id}/items/GamePass/{gamepass_id}"
    r = requests.get(url, timeout=10)
    data = r.json()
    return len(data.get("data", [])) > 0

class Payments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="create-ltc-order", description="Créer une commande LTC")
    async def create_ltc_order(self, interaction: discord.Interaction):
        if not LTC_ADDRESS:
            return await interaction.response.send_message(
                "❌ LTC_ADDRESS n'est pas configuré dans Railway.",
                ephemeral=True
            )

        data = load()
        uid = str(interaction.user.id)

        order = {
            "user_id": uid,
            "username": str(interaction.user),
            "product": PRODUCT_NAME,
            "payment": "LTC",
            "status": "pending",
            "address": LTC_ADDRESS
        }

        data["orders"].append(order)
        save(data)

        await interaction.response.send_message(
            f"💰 **Commande LTC créée**\n\n"
            f"Produit : `{PRODUCT_NAME}`\n"
            f"Adresse LTC :\n`{LTC_ADDRESS}`\n\n"
            f"Après paiement, utilise : `/check-ltc-payment`",
            ephemeral=True
        )

    @discord.app_commands.command(name="check-ltc-payment", description="Vérifier paiement LTC")
    async def check_ltc_payment(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        if not LTC_ADDRESS:
            return await interaction.followup.send("❌ LTC_ADDRESS manquant.")

        try:
            balance = get_ltc_balance(LTC_ADDRESS)
        except Exception as e:
            return await interaction.followup.send(f"❌ Erreur API LTC : {e}")

        if balance <= 0:
            return await interaction.followup.send(
                "❌ Aucun paiement LTC détecté pour l’instant."
            )

        role = discord.utils.get(interaction.guild.roles, name=CUSTOMER_ROLE_NAME)
        if role:
            await interaction.user.add_roles(role)

        try:
            await interaction.user.send(
                f"✅ **Paiement LTC détecté**\n"
                f"Produit : `{PRODUCT_NAME}`\n\n"
                f"Voici ton produit :\n"
                f"`TON LIEN OU SCRIPT ICI`"
            )
        except:
            pass

        data = load()
        data["orders"].append({
            "user_id": str(interaction.user.id),
            "username": str(interaction.user),
            "product": PRODUCT_NAME,
            "payment": "LTC",
            "status": "paid"
        })
        save(data)

        await log(interaction.guild, f"💰 Paiement LTC détecté pour {interaction.user.mention}")

        await interaction.followup.send(
            "✅ Paiement détecté. Produit envoyé en DM."
        )

    @discord.app_commands.command(name="verify-robux", description="Vérifier achat Robux via gamepass")
    async def verify_robux(
        self,
        interaction: discord.Interaction,
        username: str,
        gamepass_id: int
    ):
        await interaction.response.defer(ephemeral=True)

        try:
            user_id = username_to_id(username)

            if user_id is None:
                return await interaction.followup.send("❌ Roblox username introuvable.")

            if not owns_gamepass(user_id, gamepass_id):
                return await interaction.followup.send("❌ Gamepass non détecté.")

        except Exception as e:
            return await interaction.followup.send(f"❌ Erreur Roblox API : {e}")

        role = discord.utils.get(interaction.guild.roles, name=CUSTOMER_ROLE_NAME)
        if role:
            await interaction.user.add_roles(role)

        try:
            await interaction.user.send(
                f"✅ **Achat Robux confirmé**\n"
                f"Produit : `{PRODUCT_NAME}`\n\n"
                f"Voici ton produit :\n"
                f"`TON LIEN OU SCRIPT ICI`"
            )
        except:
            pass

        data = load()
        data["orders"].append({
            "user_id": str(interaction.user.id),
            "username": str(interaction.user),
            "roblox_username": username,
            "product": PRODUCT_NAME,
            "payment": "Robux",
            "status": "paid"
        })
        save(data)

        await log(interaction.guild, f"🎮 Achat Robux validé pour {interaction.user.mention}")

        await interaction.followup.send("✅ Achat validé. Produit envoyé en DM.")

async def setup(bot):
    await bot.add_cog(Payments(bot))
