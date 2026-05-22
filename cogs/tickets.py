import discord
from discord.ext import commands
import asyncio
from config import LOG_CHANNEL_ID

async def log(guild, message):
    channel = guild.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(message)

class TicketControl(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🛠 Claim", style=discord.ButtonStyle.blurple)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"🛠 Ticket pris par {interaction.user.mention}"
        )

    @discord.ui.button(label="🔒 Close", style=discord.ButtonStyle.gray)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.set_permissions(interaction.user, send_messages=False)

        await interaction.response.send_message("🔒 Ticket fermé.")
        await log(interaction.guild, f"🔒 Ticket fermé par {interaction.user.mention}")

    @discord.ui.button(label="🗑 Delete", style=discord.ButtonStyle.red)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🗑 Suppression dans 3 secondes...")
        await log(interaction.guild, f"🗑 Ticket supprimé par {interaction.user.mention}")
        await asyncio.sleep(3)
        await interaction.channel.delete()

class TicketPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def create_ticket(self, interaction, reason):
        guild = interaction.guild

        category = discord.utils.get(guild.categories, name="🎫 OKVEHUB TICKETS")
        if category is None:
            category = await guild.create_category("🎫 OKVEHUB TICKETS")

        name = f"ticket-{interaction.user.name}".lower()

        existing = discord.utils.get(guild.text_channels, name=name)
        if existing:
            return await interaction.response.send_message(
                f"❌ Tu as déjà un ticket : {existing.mention}",
                ephemeral=True
            )

        channel = await guild.create_text_channel(name=name, category=category)

        await channel.set_permissions(guild.default_role, read_messages=False)
        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await channel.set_permissions(guild.me, read_messages=True, send_messages=True)

        embed = discord.Embed(
            title="🎫 OKVEHUB SUPPORT",
            description=(
                f"Bienvenue {interaction.user.mention}\n\n"
                f"📌 Type : `{reason}`\n\n"
                "Explique ton problème clairement.\n\n"
                "🛠 Claim\n"
                "🔒 Close\n"
                "🗑 Delete"
            ),
            color=0x00aaff
        )

        await channel.send(
            content=interaction.user.mention,
            embed=embed,
            view=TicketControl()
        )

        await log(guild, f"🎫 Ticket ouvert par {interaction.user.mention} | {reason}")

        await interaction.response.send_message(
            f"✅ Ticket créé : {channel.mention}",
            ephemeral=True
        )

    @discord.ui.button(label="🛒 Achat", style=discord.ButtonStyle.green)
    async def achat(self, interaction, button):
        await self.create_ticket(interaction, "achat")

    @discord.ui.button(label="💰 Paiement", style=discord.ButtonStyle.blurple)
    async def paiement(self, interaction, button):
        await self.create_ticket(interaction, "paiement")

    @discord.ui.button(label="🐞 Bug", style=discord.ButtonStyle.red)
    async def bug(self, interaction, button):
        await self.create_ticket(interaction, "bug")

    @discord.ui.button(label="❓ Question", style=discord.ButtonStyle.gray)
    async def question(self, interaction, button):
        await self.create_ticket(interaction, "question")

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ticket-panel", description="Envoyer le panel ticket")
    async def ticket_panel(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎫 OKVEHUB SUPPORT CENTER",
            description=(
                "Choisis une catégorie :\n\n"
                "🛒 Achat\n"
                "💰 Paiement\n"
                "🐞 Bug\n"
                "❓ Question"
            ),
            color=0x3498db
        )

        await interaction.response.send_message("✅ Panel envoyé.", ephemeral=True)
        await interaction.channel.send(embed=embed, view=TicketPanel())

    @discord.app_commands.command(name="close-ticket", description="Fermer ce ticket")
    async def close_ticket(self, interaction: discord.Interaction):
        if not interaction.channel.name.startswith("ticket-"):
            return await interaction.response.send_message("❌ Ce salon n'est pas un ticket.", ephemeral=True)

        await interaction.channel.set_permissions(interaction.user, send_messages=False)
        await interaction.response.send_message("🔒 Ticket fermé.")

    @discord.app_commands.command(name="delete-ticket", description="Supprimer ce ticket")
    async def delete_ticket(self, interaction: discord.Interaction):
        if not interaction.channel.name.startswith("ticket-"):
            return await interaction.response.send_message("❌ Ce salon n'est pas un ticket.", ephemeral=True)

        await interaction.response.send_message("🗑 Suppression dans 3 secondes...")
        await asyncio.sleep(3)
        await interaction.channel.delete()

async def setup(bot):
    await bot.add_cog(Tickets(bot))
