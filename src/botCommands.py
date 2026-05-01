import os
import discord
from discord import Intents
from discord.ext import commands
from src.modals.AddGameComplete import AddGameCompleteModal
from src.modals.Birthday import BirthdayModal
from src.util.commandUtil import getBirthdays, getCompletedGames, sortBirthdays,sortGames
from src.util.logging import log_command
from src.views.basicPaginator.BasicPaginator import BasicPaginator


def setup(intents: Intents) -> commands.Bot:
	bot = commands.Bot(command_prefix="!", intents=intents)
	
	@bot.tree.command(name="birth", description="Set your birthday")
	@log_command
	async def birth(interaction: discord.Interaction):
		await interaction.response.send_modal(BirthdayModal())

	@bot.tree.command(name="complete")
	@log_command
	async def complete(interaction: discord.Interaction):
		await interaction.response.send_modal(AddGameCompleteModal())

	@bot.tree.command(name="completed", description="List all the games you've completed")
	@log_command
	async def completed(interaction: discord.Interaction, member:discord.Member = None, hide:bool = True):
		if member is None:
			member = interaction.user
		gamesComplete = await getCompletedGames(interaction.guild.id, member.id)
		if not gamesComplete:
			await interaction.response.send_message(
				f"{member.mention} hasn't completed any games yet. Use /complete to add a completed game!",
				ephemeral=hide
			)
			return
		sorted_games = await sortGames(gamesComplete)
		print(sorted_games)
		game_list = []
		for game_data in sorted_games:
			title = game_data.get("title")
			platform = game_data.get("platform")
			date = game_data.get("completionDate")
			game_list.append(f"**{title}** on **{platform}** completed on {date}")
		chunk_size = 10
		pages = [
			"\n".join(game_list[i:i + chunk_size])
			for i in range(0, len(game_list), chunk_size)
		]
		view = BasicPaginator(pages)
		await interaction.response.send_message(content=pages[0], view=view, ephemeral=hide)
		

	@bot.tree.command(name="joined", description="Get the date a member joined")
	@log_command
	async def joined(interaction: discord.Interaction, member: discord.Member):
		await interaction.response.send_message(
			f'{member} joined on {member.joined_at.date()}'
    )
	
	@bot.tree.command(name="birthdays", description="Get the birthdays of members")
	@log_command
	async def birthdays(interaction: discord.Interaction,hide:bool = True):
		users = await getBirthdays(interaction.guild.id)
		if not users:
			await interaction.response.send_message(
				"No birthdays found for this server.",
				ephemeral=hide
			)
			return
		sorted_users = await sortBirthdays(users)
		birthday_list = []
		print(sorted_users)
		for user_id, user_data in sorted_users:
			birthday = user_data.get("birthday")
			user = await bot.fetch_user(int(user_id))
			birthday_list.append(f"{user.name}: {birthday}")

		chunk_size = 10
		pages = [
			"\n".join(birthday_list[i:i + chunk_size])
			for i in range(0, len(birthday_list), chunk_size)
		]
		view = BasicPaginator(pages)
		await interaction.response.send_message(content=pages[0], view=view, ephemeral=hide)
		
	@bot.tree.command(name="slap", description="Slap crystal")
	@log_command
	async def slap(interaction: discord.Interaction):
		user = await bot.fetch_user(int(os.getenv("SLAP_USER_ID")))
		await interaction.response.send_message(f'{interaction.user} slapped {user.mention}!')

	@bot.tree.command(name="hug", description="Hug Peter")
	@log_command
	async def hug(interaction: discord.Interaction):
		user = await bot.fetch_user(int(os.getenv("HUG_USER_ID")))
		await interaction.response.send_message(f'{interaction.user} hugged {user.mention}!')

	@bot.tree.command(name="pants", description="Pants...")
	@log_command
	async def pants(interaction: discord.Interaction):
		user = await bot.fetch_user(int(os.getenv("PANTS_USER_ID")))
		await interaction.response.send_message(f'{interaction.user} told {user.mention} to put some pants on!')

	@bot.tree.command(name="shame", description="Shame a member")
	@log_command
	async def shame(interaction: discord.Interaction, member: discord.Member = None):
		gif = "https://tenor.com/view/we-dont-do-that-here-black-panther-tchalla-bruce-gif-16558003"
		if member:
			await interaction.response.send_message(f"{member.mention} \n {gif}")
		else:
			await interaction.response.send_message(gif)

	# @bot.tree.command(name="server_info", description="Get server information")
	# async def server_info(interaction: discord.Interaction):
	# 	if interaction.guild:
	# 		guild_name = interaction.guild.name
	# 		guild_id = interaction.guild.id
	# 		await interaction.response.send_message(f"This server is: {guild_name} (ID: {guild_id})")
	# 	else:
	# 		await interaction.response.send_message("This command was used in a DM!")
	

	return bot
