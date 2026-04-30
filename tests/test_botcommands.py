import inspect
import unittest
from unittest.mock import AsyncMock, MagicMock
import discord
from discord import Intents
from src import botCommands
from unittest.mock import AsyncMock
import os

def with_dialogue(func):
    if inspect.iscoroutinefunction(func):
        async def async_wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                print(f"\n[BOT]: 'Scanning {func.__name__}... Success!'")
                return result
            except Exception as e:
                print(f"\n[BOT]: 'Scanning {func.__name__}... Failed!'")
                raise e
        return async_wrapper
    else:
        def sync_wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                print(f"\n[BOT]: 'Scanning {func.__name__}... Success!'")
                return result
            except Exception as e:
                print(f"\n[BOT]: 'Scanning {func.__name__}... Failed!'")
                raise e
            
        return sync_wrapper
class TestBotCommands(unittest.IsolatedAsyncioTestCase):
    @with_dialogue
    def test_setup_returns_bot(self):
        intents = Intents.default()
        bot = botCommands.setup(intents)
        self.assertTrue(hasattr(bot, "tree"))
        
    @with_dialogue
    async def test_joined_command(self):
        intents = discord.Intents.default()
        bot = botCommands.setup(intents)

        joined_cmd = [cmd.callback for cmd in bot.tree.get_commands() if cmd.name == "joined"][0]
        mock_interaction = MagicMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_member = MagicMock()
        mock_member.__str__.return_value = "TestUser"
        mock_member.joined_at = "2022-01-01"
        await joined_cmd(mock_interaction, mock_member)
        mock_interaction.response.send_message.assert_awaited_with("TestUser joined on 2022-01-01")

    @with_dialogue
    async def test_hug_command(self):
        os.environ["HUG_USER_ID"] = "123456789"
        intents = discord.Intents.default()
        bot = botCommands.setup(intents)

        hug_cmd = [cmd.callback for cmd in bot.tree.get_commands() if cmd.name == "hug"][0]
        mock_interaction = AsyncMock()
        mock_interaction.user = AsyncMock()
        mock_interaction.user.name = "Tester"
        mock_interaction.mention = "@TestUser"
        bot.fetch_user = AsyncMock(return_value=mock_interaction)
        await hug_cmd(mock_interaction)
        mock_interaction.response.send_message.assert_awaited_with(f'{mock_interaction.user} hugged {mock_interaction.mention}!')
    
    @with_dialogue
    async def test_slap_command(self):
        os.environ["SLAP_USER_ID"] = "123456789"
        intents = discord.Intents.default()
        bot = botCommands.setup(intents)
        slap_cmd = [cmd.callback for cmd in bot.tree.get_commands() if cmd.name == "slap"][0]
        mock_interaction = AsyncMock()
        mock_interaction.response.send_message = AsyncMock()
        bot.fetch_user = AsyncMock(return_value=mock_interaction)
        await slap_cmd(mock_interaction)
        mock_interaction.response.send_message.assert_awaited_with(f'{mock_interaction.user} slapped {mock_interaction.mention}!')
    
    @with_dialogue
    async def test_shame_command(self):
        intents = discord.Intents.default()
        bot = botCommands.setup(intents)
        shame_cmd = [cmd.callback for cmd in bot.tree.get_commands() if cmd.name == "shame"][0]
        mock_interaction = AsyncMock()
        mock_interaction.response.send_message = AsyncMock()
        bot.fetch_user = AsyncMock(return_value=mock_interaction)
        await shame_cmd(mock_interaction)
        mock_interaction.response.send_message.assert_awaited_with(f'https://tenor.com/view/we-dont-do-that-here-black-panther-tchalla-bruce-gif-16558003')

    @with_dialogue
    async def test_shame_mention_command(self):
        intents = discord.Intents.default()
        bot = botCommands.setup(intents)
        shame_cmd = [cmd.callback for cmd in bot.tree.get_commands() if cmd.name == "shame"][0]
        mock_interaction = AsyncMock()
        mock_interaction.response.send_message = AsyncMock()
        bot.fetch_user = AsyncMock(return_value=mock_interaction)
        await shame_cmd(mock_interaction,mock_interaction)
        mock_interaction.response.send_message.assert_awaited_with(f'{mock_interaction.mention} \n https://tenor.com/view/we-dont-do-that-here-black-panther-tchalla-bruce-gif-16558003')

    @with_dialogue
    async def test_birthdays_command_no_birthdays(self):
        intents = discord.Intents.default()
        bot = botCommands.setup(intents)
        birthdays_cmd = [cmd.callback for cmd in bot.tree.get_commands() if cmd.name == "birthdays"][0]
        mock_interaction = AsyncMock()
        mock_interaction.response.send_message = AsyncMock()
        bot.fetch_user = AsyncMock(return_value=mock_interaction)
        await birthdays_cmd(mock_interaction)
        mock_interaction.response.send_message.assert_awaited_with("No birthdays found for this server.", ephemeral=True)
        
    @with_dialogue
    async def test_birthdays_command_with_birthdays(self):
        intents = discord.Intents.default()
        bot = botCommands.setup(intents)
        birthdays_cmd = [
            cmd.callback for cmd in bot.tree.get_commands()
            if cmd.name == "birthdays"
        ][0]
        mock_interaction = AsyncMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_user = MagicMock()
        mock_user.name = "TestUser"
        botCommands.getBirthdays = AsyncMock(return_value={
        "1": "2000-01-01"
        })
        botCommands.sortBirthdays = AsyncMock(return_value=[
            ("1", {"birthday": "2000-01-01"})
        ])
        bot.fetch_user = AsyncMock(return_value=mock_user)
        await birthdays_cmd(mock_interaction)
        mock_interaction.response.send_message.assert_awaited_with(
            content="TestUser: 2000-01-01",
            view=unittest.mock.ANY,
            ephemeral=True
        )
if __name__ == "__main__":
    unittest.main()