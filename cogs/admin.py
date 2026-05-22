import discord
from discord.ext import commands
from database import load, save
from config import LOG_CHANNEL_ID

async def send_log(guild, message):
    channel = guild.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(message)

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_admin(self, interaction):
        return interaction.user.guild_permissions.administrator

    @discord.app_commands.command(name="add-brainrot", description="Ajouter du Brainrot")
    async def add_brainrot(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        if not self.is_admin(interaction):
            return await interaction.response.send_message("❌ Admin only.", ephemeral=True)

        data = load()
        uid = str(user.id)

        data["brainrot"][uid] = data["brainrot"].get(uid, 0) + amount
        save(data)

        await send_log(
            interaction.guild,
            f"🧪 {amount} Brainrot ajouté à {user.mention} par {interaction.user.mention}"
        )

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

        embed = discord.Embed(
            title="🧪 OKVEHUB BALANCE",
            description=f"Ta balance : `{balance}` Brainrot",
            color=0x9b59b6
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.app_commands.command(name="orders", description="Voir les dernières commandes")
    async def orders(self, interaction: discord.Interaction):
        if not self.is_admin(interaction):
            return await interaction.response.send_message("❌ Admin only.", ephemeral=True)

        data = load()
        orders = data.get("orders", [])[-10:]

        if not orders:
            return await interaction.response.send_message("Aucune commande.", ephemeral=True)

        text = ""

        for order in orders:
            text += (
                f"• `{order.get('payment')}` | "
                f"`{order.get('status')}` | "
                f"`{order.get('product')}` | "
                f"`{order.get('user')}`\n"
            )

        embed = discord.Embed(
            title="📊 LAST ORDERS",
            description=text,
            color=0xffcc00
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Admin(bot))
