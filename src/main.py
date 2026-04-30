
import json
import botCommands
import os
from dotenv import load_dotenv
import discord
from tasks.birthdayCheck import checkBirthdays


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
        synced = await bot.tree.sync()
        bot.loop.create_task(checkBirthdays(bot))
        print(f"Synced {len(synced)} commands")    

    except Exception as e:
        print(f"Error syncing commands: {e}")

bot.run(os.getenv('TOKEN'))