import discord
from discord.ext import commands
from config import LOG_CHANNEL_NAME

async def send_log(guild, text):
    channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
    if channel:
        await channel.send(text)

class TicketControlView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🛠 Claim", style=discord.ButtonStyle.blurple)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🛠 Ticket Claim",
            description=f"Ce ticket est maintenant pris par {interaction.user.mention}",
            color=0x5865F2
        )
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="🔒 Close", style=discord.ButtonStyle.gray)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.set_permissions(interaction.guild.default_role, read_messages=False)
        await interaction.channel.set_permissions(interaction.user, send_messages=False)

        embed = discord.Embed(
            title="🔒 Ticket fermé",
            description="Le ticket est fermé. Tu peux le supprimer avec le bouton rouge.",
            color=0xffcc00
        )

        await send_log(interaction.guild, f"🔒 Ticket fermé : `{interaction.channel.name}` par {interaction.user.mention}")
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="🗑 Delete", style=discord.ButtonStyle.red)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🗑 Suppression du ticket dans 3 secondes...")
        await send_log(interaction.guild, f"🗑 Ticket supprimé : `{interaction.channel.name}` par {interaction.user.mention}")

        import asyncio
        await asyncio.sleep(3)
        await interaction.channel.delete()

class TicketPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🛒 Achat", style=discord.ButtonStyle.green)
    async def achat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "achat")

    @discord.ui.button(label="💰 Paiement", style=discord.ButtonStyle.blurple)
    async def paiement(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "paiement")

    @discord.ui.button(label="🐞 Bug", style=discord.ButtonStyle.red)
    async def bug(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "bug")

    @discord.ui.button(label="❓ Question", style=discord.ButtonStyle.gray)
    async def question(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "question")

    async def create_ticket(self, interaction: discord.Interaction, reason: str):
        guild = interaction.guild

        category = discord.utils.get(guild.categories, name="🎫 OKVEHUB TICKETS")
        if not category:
            category = await guild.create_category("🎫 OKVEHUB TICKETS")

        existing = discord.utils.get(
            guild.text_channels,
            name=f"ticket-{interaction.user.name}".lower()
        )

        if existing:
            return await interaction.response.send_message(
                f"❌ Tu as déjà un ticket : {existing.mention}",
                ephemeral=True
            )

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category
        )

        await channel.set_permissions(guild.default_role, read_messages=False)
        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await channel.set_permissions(guild.me, read_messages=True, send_messages=True)

        embed = discord.Embed(
            title="🎫 OKVEHUB SUPPORT",
            description=(
                f"Bienvenue {interaction.user.mention}\n\n"
                f"📌 Type : `{reason}`\n"
                "📝 Explique ton problème clairement.\n\n"
                "**Boutons disponibles :**\n"
                "🛠 Claim = staff prend le ticket\n"
                "🔒 Close = fermer\n"
                "🗑 Delete = supprimer"
            ),
            color=0x00aaff
        )

        embed.set_footer(text="OkveHUB Support System")

        await channel.send(
            content=interaction.user.mention,
            embed=embed,
            view=TicketControlView()
        )

        await send_log(guild, f"🎫 Ticket ouvert par {interaction.user.mention} | Type : `{reason}`")

        await interaction.response.send_message(
            f"✅ Ticket créé : {channel.mention}",
            ephemeral=True
        )

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ticket-panel", description="Afficher le panel ticket OkveHUB")
    async def ticket_panel(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎫 OKVEHUB SUPPORT CENTER",
            description=(
                "```ansi\n"
                "[1;34m╔══════════════════════╗[0m\n"
                "[1;36m     SUPPORT CENTER    [0m\n"
                "[1;34m╚══════════════════════╝[0m\n"
                "```\n"
                "Besoin d'aide ? Choisis une catégorie :\n\n"
                "🛒 **Achat** — acheter OkveHUB\n"
                "💰 **Paiement** — problème LTC / Robux / Brainrot\n"
                "🐞 **Bug** — bug avec le script\n"
                "❓ **Question** — question générale\n\n"
                "Un salon privé sera créé automatiquement."
            ),
            color=0x3498db
        )

        embed.set_footer(text="OkveHUB • Fast Support")

        await interaction.channel.send(embed=embed, view=TicketPanelView())
        await interaction.response.send_message("✅ Panel ticket PRO envoyé.", ephemeral=True)

    @discord.app_commands.command(name="close-ticket", description="Fermer le ticket actuel")
    async def close_ticket(self, interaction: discord.Interaction):
        if not interaction.channel.name.startswith("ticket-"):
            return await interaction.response.send_message("❌ Ce salon n'est pas un ticket.", ephemeral=True)

        await interaction.channel.set_permissions(interaction.guild.default_role, read_messages=False)
        await interaction.response.send_message("🔒 Ticket fermé.")

    @discord.app_commands.command(name="delete-ticket", description="Supprimer le ticket actuel")
    async def delete_ticket(self, interaction: discord.Interaction):
        if not interaction.channel.name.startswith("ticket-"):
            return await interaction.response.send_message("❌ Ce salon n'est pas un ticket.", ephemeral=True)

        await interaction.response.send_message("🗑 Suppression dans 3 secondes...")

        import asyncio
        await asyncio.sleep(3)
        await interaction.channel.delete()

async def setup(bot):
    await bot.add_cog(Tickets(bot))
