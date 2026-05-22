import discord
from discord.ext import commands

class ShopView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="💰 Litecoin",
        style=discord.ButtonStyle.green
    )
    async def ltc(self, interaction, button):

        await interaction.response.send_message(
            "💰 LTC payment selected",
            ephemeral=True
        )

    @discord.ui.button(
        label="🎮 Robux",
        style=discord.ButtonStyle.blurple
    )
    async def robux(self, interaction, button):

        await interaction.response.send_message(
            "🎮 Robux selected",
            ephemeral=True
        )

    @discord.ui.button(
        label="🧪 Brainrot",
        style=discord.ButtonStyle.red
    )
    async def brainrot(self, interaction, button):

        await interaction.response.send_message(
            "🧪 Brainrot selected",
            ephemeral=True
        )

class Shop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="shop",
        description="Open shop panel"
    )
    async def shop(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="🛒 SHOP PANEL",
            description="Choose payment method",
            color=0x00ff00
        )

        await interaction.channel.send(
            embed=embed,
            view=ShopView()
        )

        await interaction.response.send_message(
            "✅ Shop panel sent",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Shop(bot))
