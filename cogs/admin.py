import discord
from discord.ext import commands
from database import load, save
from config import LOG_CHANNEL_NAME

async def log(guild, message):
    channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
    if channel:
        await channel.send(message)

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_admin(self, interaction):
        return interaction.user.guild_permissions.administrator

    @discord.app_commands.command(name="add-brainrot", description="Ajouter du Brainrot à un membre")
    async def add_brainrot(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        if not self.is_admin(interaction):
            return await interaction.response.send_message("❌ Admin only.", ephemeral=True)

        data = load()
        uid = str(user.id)

        data["brainrot"][uid] = data["brainrot"].get(uid, 0) + amount
        save(data)

        await log(interaction.guild, f"🧪 {amount} Brainrot ajouté à {user.mention}")

        await interaction.response.send_message(
            f"✅ `{amount}` Brainrot ajouté à {user.mention}",
            ephemeral=True
        )

    @discord.app_commands.command(name="remove-brainrot", description="Retirer du Brainrot")
    async def remove_brainrot(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        if not self.is_admin(interaction):
            return await interaction.response.send_message("❌ Admin only.", ephemeral=True)

        data = load()
        uid = str(user.id)

        data["brainrot"][uid] = max(0, data["brainrot"].get(uid, 0) - amount)
        save(data)

        await interaction.response.send_message(
            f"✅ `{amount}` Brainrot retiré à {user.mention}",
            ephemeral=True
        )

    @discord.app_commands.command(name="balance", description="Voir sa balance Brainrot")
    async def balance(self, interaction: discord.Interaction):
        data = load()
        uid = str(interaction.user.id)

        balance = data["brainrot"].get(uid, 0)

        await interaction.response.send_message(
            f"🧪 Ta balance : `{balance}` Brainrot",
            ephemeral=True
        )

    @discord.app_commands.command(name="orders", description="Voir les commandes")
    async def orders(self, interaction: discord.Interaction):
        if not self.is_admin(interaction):
            return await interaction.response.send_message("❌ Admin only.", ephemeral=True)

        data = load()
        orders = data.get("orders", [])[-10:]

        if not orders:
            return await interaction.response.send_message("Aucune commande.", ephemeral=True)

        text = ""

        for order in orders:
            text += f"• `{order.get('payment')}` - `{order.get('status')}` - {order.get('username')}\n"

        await interaction.response.send_message(text, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Admin(bot))
