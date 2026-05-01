import discord

from discord.ui import Modal, TextInput
from src.util.commandUtil import setBirthday

class BirthdayModal(Modal, title="Enter Your Birthday"):
    year = TextInput(label="Year", placeholder="e.g. 2005", required=False)
    month = TextInput(label="Month (1-12)", required=True)
    day = TextInput(label="Day (1-31)", required=True)
    async def on_submit(self, interaction: discord.Interaction):
        try:
            year = int(self.year.value) if self.year.value else None
            month = int(self.month.value)
            day = int(self.day.value)
            if month < 1 or month > 12:
                await interaction.response.send_message("Invalid month (1-12). please try again.", ephemeral=True)
                return

            if day < 1 or day > 31:
                await interaction.response.send_message("Invalid day (1-31). please try again.", ephemeral=True)
                return

        except ValueError:
            await interaction.response.send_message("Numbers only please.", ephemeral=True)
            return
        birthday = f"{day:02d}/{month:02d}/{year}" if year else f"{day:02d}/{month:02d}"
        response = await setBirthday(interaction.guild.id, interaction.user.id, birthday)
        if response:
            await interaction.response.send_message(
                f"Birthday saved: {birthday}", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "Failed to save birthday. please try again.", ephemeral=True
            )