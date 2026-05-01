
import json
import botCommands as botCommands
import os
from dotenv import load_dotenv
import discord
from tasks.birthdayCheck import checkBirthdays
import logging
from util.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

db_path = os.path.join(os.path.dirname(__file__), '..', 'src/db.json')
db_path = os.path.abspath(db_path)
if not os.path.exists(db_path):
    with open(db_path, 'w') as f:
        data = {}
        json.dump(data, f)

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = botCommands.setup(intents)

@bot.event
async def on_ready():
    try:
        # await bot.tree.sync(guild=discord.Object(id=774522422669344798))
        synced = await bot.tree.sync()
        bot.loop.create_task(checkBirthdays(bot))
        logger.info(f"Synced {len(synced)} commands")    

    except Exception as e:
        logger.error(f"Error syncing commands: {e}", exc_info=True)

bot.run(os.getenv('TOKEN'))