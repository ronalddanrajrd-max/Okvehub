import discord
from discord.ext import commands
import asyncio
import requests
from database import load, save
from config import (
    LTC_ADDRESS,
    LTC_PRICE,
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

async def send_log(guild, message):
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

class ShopView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="💰 Litecoin", style=discord.ButtonStyle.green)
    async def ltc(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        try:
            before_balance = ltc_balance(LTC_ADDRESS)
        except Exception as e:
            return await interaction.followup.send(
                f"❌ Erreur API LTC : `{e}`",
                ephemeral=True
            )

        embed = discord.Embed(
            title="💰 OKVEHUB LTC PAYMENT",
            description=(
                "🔐 **Commande sécurisée créée**\n\n"
                f"💵 Prix : `{LTC_PRICE}` litoshis\n"
                f"📥 Adresse LTC :\n`{LTC_ADDRESS}`\n\n"
                "⏳ Le bot scanne automatiquement le paiement."
            ),
            color=0x00ff99
        )

        msg = await interaction.followup.send(embed=embed, ephemeral=True)

        for i in range(60):
            await asyncio.sleep(10)

            try:
                current_balance = ltc_balance(LTC_ADDRESS)
                received = current_balance - before_balance
            except Exception as e:
                embed.title = "⚠️ LTC API ERROR"
                embed.description = f"Erreur temporaire : `{e}`\nLe scan continue..."
                embed.color = 0xff9900
                await msg.edit(embed=embed)
                continue

            embed.title = "🔄 LTC PAYMENT SCANNING"
            embed.description = (
                "```ansi\n"
                "\u001b[1;32m╔══════════════════════╗\u001b[0m\n"
                "\u001b[1;36m     BLOCKCHAIN SCAN    \u001b[0m\n"
                "\u001b[1;32m╚══════════════════════╝\u001b[0m\n"
                "```\n"
                f"💵 Prix : `{LTC_PRICE}` litoshis\n"
                f"📥 Reçu : `{received}` litoshis\n"
                f"📍 Adresse :\n`{LTC_ADDRESS}`\n\n"
                f"⏳ Scan : `{i + 1}/60`"
            )
            embed.color = 0xffcc00

            await msg.edit(embed=embed)

            if received >= LTC_PRICE:
                data = load()
                data["orders"].append({
                    "user": str(interaction.user),
                    "user_id": str(interaction.user.id),
                    "payment": "LTC",
                    "price": LTC_PRICE,
                    "product": PRODUCT_NAME,
                    "status": "paid"
                })
                save(data)

                await give_customer(interaction.user)
                await deliver(interaction.user)

                await send_log(
                    interaction.guild,
                    f"💰 Paiement LTC validé automatiquement pour {interaction.user.mention}"
                )

                embed.title = "✅ PAYMENT CONFIRMED"
                embed.description = (
                    "✅ Paiement LTC détecté automatiquement.\n\n"
                    "📦 Produit envoyé en DM.\n"
                    "🎖 Rôle Customer ajouté."
                )
                embed.color = 0x00ff00

                await msg.edit(embed=embed)
                return

        embed.title = "⏱ PAYMENT TIMEOUT"
        embed.description = (
            "❌ Aucun paiement détecté après 10 minutes.\n\n"
            "Si tu as payé, ouvre un ticket support."
        )
        embed.color = 0xff0000

        await msg.edit(embed=embed)

    @discord.ui.button(label="🎮 Robux", style=discord.ButtonStyle.blurple)
    async def robux(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🎮 OKVEHUB ROBUX PAYMENT",
            description=(
                "1️⃣ Achète le gamepass Roblox\n"
                "2️⃣ Utilise la commande :\n"
                "`/verify-robux username gamepass_id`\n\n"
                "✅ Si le gamepass est détecté :\n"
                "📦 Livraison DM\n"
                "🎖 Rôle Customer"
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
                f"❌ Balance insuffisante.\nTu as : `{balance}` Brainrot",
                ephemeral=True
            )

        data["brainrot"][uid] -= BRAINROT_PRICE
        data["orders"].append({
            "user": str(interaction.user),
            "user_id": uid,
            "payment": "Brainrot",
            "price": BRAINROT_PRICE,
            "product": PRODUCT_NAME,
            "status": "paid"
        })
        save(data)

        await give_customer(interaction.user)
        await deliver(interaction.user)

        await send_log(
            interaction.guild,
            f"🧪 Paiement Brainrot validé pour {interaction.user.mention}"
        )

        await interaction.response.send_message(
            "✅ Paiement Brainrot validé. Produit envoyé en DM.",
            ephemeral=True
        )

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="shop", description="Envoyer le panel shop OkveHUB")
    async def shop(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="💎 OKVEHUB PREMIUM SHOP",
            description=(
                "```ansi\n"
                "\u001b[1;35m╔══════════════════════╗\u001b[0m\n"
                "\u001b[1;36m       OKVEHUB PRO      \u001b[0m\n"
                "\u001b[1;35m╚══════════════════════╝\u001b[0m\n"
                "```\n"
                "🔥 **Script premium**\n\n"
                "⚡ Livraison automatique\n"
                "🔐 Paiements sécurisés\n"
                "🎖 Rôle Customer automatique\n"
                "📦 Delivery en DM\n\n"
                "**Méthodes disponibles :**\n"
                "💰 Litecoin auto-scan\n"
                "🎮 Robux Gamepass\n"
                "🧪 Brainrot Wallet"
            ),
            color=0x9b59b6
        )

        embed.set_footer(text="OkveHUB • Automated Premium System")

        await interaction.response.send_message("✅ Panel shop envoyé.", ephemeral=True)
        await interaction.channel.send(embed=embed, view=ShopView())

async def setup(bot):
    await bot.add_cog(Shop(bot))
