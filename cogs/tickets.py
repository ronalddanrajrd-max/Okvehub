import discord
from discord.ext import commands

class TicketView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="🎫 Open Ticket",
        style=discord.ButtonStyle.green
    )
    async def open_ticket(self, interaction, button):

        guild = interaction.guild

        category = discord.utils.get(
            guild.categories,
            name="TICKETS"
        )

        if not category:
            category = await guild.create_category("TICKETS")

        channel = await guild.create_text_channel(
            f"ticket-{interaction.user.name}",
            category=category
        )

        await channel.set_permissions(
            interaction.user,
            read_messages=True,
            send_messages=True
        )

        await channel.send(
            f"🎫 Welcome {interaction.user.mention}"
        )

        await interaction.response.send_message(
            f"✅ Ticket created: {channel.mention}",
            ephemeral=True
        )

class Tickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="ticket-panel",
        description="Create ticket panel"
    )
    async def ticket_panel(self, interaction):

        await interaction.channel.send(
            "🎫 SUPPORT PANEL",
            view=TicketView()
        )

        await interaction.response.send_message(
            "✅ Panel sent",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Tickets(bot))
