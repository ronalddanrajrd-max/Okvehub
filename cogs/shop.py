import discord
from discord.ext import commands
from database import load, save
from config import CUSTOMER_ROLE_NAME, LOG_CHANNEL_NAME

PRODUCT_NAME = "Premium Script"
PRODUCT_PRICE_BRAINROT = 1

async def log(guild, message):
    channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
    if channel:
        await channel.send(message)

class ShopView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="💰 Pay LTC", style=discord.ButtonStyle.green)
    async def pay_ltc(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "💰 **LTC Payment**\n"
            "Utilise la commande :\n"
            "`/create-ltc-order`\n\n"
            "Le bot va créer une commande et vérifier le paiement.",
            ephemeral=True
        )

    @discord.ui.button(label="🎮 Pay Robux", style=discord.ButtonStyle.blurple)
    async def pay_robux(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "🎮 **Robux Payment**\n"
            "Après achat du gamepass, utilise :\n"
            "`/verify-robux username gamepass_id`",
            ephemeral=True
        )

    @discord.ui.button(label="🧪 Pay Brainrot", style=discord.ButtonStyle.red)
    async def pay_brainrot(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = load()
        uid = str(interaction.user.id)
        balance = data["brainrot"].get(uid, 0)

        if balance < PRODUCT_PRICE_BRAINROT:
            return await interaction.response.send_message(
                f"❌ Balance insuffisante.\nTu as : `{balance}` Brainrot",
                ephemeral=True
            )

        data["brainrot"][uid] -= PRODUCT_PRICE_BRAINROT

        data["orders"].append({
            "user_id": uid,
            "username": str(interaction.user),
            "product": PRODUCT_NAME,
            "payment": "Brainrot",
            "status": "paid"
        })

        save(data)

        role = discord.utils.get(interaction.guild.roles, name=CUSTOMER_ROLE_NAME)
        if role:
            await interaction.user.add_roles(role)

        try:
            await interaction.user.send(
                f"✅ **Achat confirmé**\n"
                f"Produit : `{PRODUCT_NAME}`\n\n"
                f"Voici ton produit :\n"
                f"`TON LIEN OU SCRIPT ICI`"
            )
        except:
            pass

        await log(interaction.guild, f"✅ {interaction.user.mention} a acheté avec Brainrot.")

        await interaction.response.send_message(
            "✅ Achat validé. Produit envoyé en DM.",
            ephemeral=True
        )

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="shop", description="Créer le panel shop")
    async def shop(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🛒 PREMIUM SHOP",
            description=(
                "**Choisis ton moyen de paiement :**\n\n"
                "💰 Litecoin\n"
                "🎮 Robux\n"
                "🧪 Brainrot\n\n"
                "Après paiement, le bot donne le rôle Customer + livraison DM."
            ),
            color=0x00ff99
        )

        embed.set_footer(text="Secure automated shop system")

        await interaction.channel.send(embed=embed, view=ShopView())
        await interaction.response.send_message("✅ Panel shop envoyé.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Shop(bot))
