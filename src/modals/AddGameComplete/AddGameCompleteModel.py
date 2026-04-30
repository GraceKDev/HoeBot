from datetime import datetime
import discord
from discord.ui import Modal
from util.commandUtil import addGameCompleted

class AddGameCompleteModel(Modal, title="Add Completed Game"):
    gameTitle = discord.ui.TextInput(label="Game Title", min_length=1, max_length=50, required=True)
    platform = discord.ui.TextInput(label="Platform", min_length=1, max_length=20, required=True)
    date = discord.ui.TextInput(label="Date", placeholder="DD/MM/YYYY", min_length=10, max_length=10, required=True)

    async def on_submit(self, interaction: discord.Interaction):

        raw_date = self.date.value.strip()
        print(raw_date)
        if len(raw_date) != 10 or raw_date[2] != "/" or raw_date[5] != "/":
            await interaction.response.send_message(
                "Invalid format. Use DD/MM/YYYY",
                ephemeral=True
            )
            return
        
        try:
            parsed_date = datetime.strptime(raw_date, "%d/%m/%Y").date()
        except ValueError:
            await interaction.response.send_message(
                "Invalid date. That date doesn't exist.",
                ephemeral=True
            )
            return

        if parsed_date > datetime.now().date():
            await interaction.response.send_message(
                "Date cannot be in the future.",
                ephemeral=True
            )
            return

        game_data = {
            "title": self.gameTitle.value,
            "platform": self.platform.value,
            "completionDate": self.date.value
        }

        response = await addGameCompleted(interaction.guild.id,interaction.user.id,game_data)
        if not response:
            await interaction.response.send_message("Failed to save game completion. Please try again.",ephemeral=True)
            return

        await interaction.response.send_message(
            f"{interaction.user.mention} just completed **{game_data['title']}** on **{game_data['platform']}** on {game_data['completionDate']}! Congratulations! 🎉",
            ephemeral=False
        )