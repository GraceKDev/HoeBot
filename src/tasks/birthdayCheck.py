import asyncio 
import datetime
import json 
import pytz

AEST = pytz.timezone('Australia/Sydney')
async def checkBirthdays(bot):
    while True:
        now = datetime.datetime.now(AEST)
        current_date = now.strftime("%Y/%m/%d")
        current_date_month_day = now.strftime("%m/%d")
        try:
            with open('src/db.json', 'r') as f:
                data = json.load(f)
            for guild_id, users in data.items():
                for user_id, birthday in users.items():
                    if birthday == current_date or birthday == current_date_month_day:
                        guild = bot.get_guild(int(guild_id))
                        member = guild.get_member(int(user_id))
                        if member:
                            await guild.system_channel.send(f"It's {member.mention}'s birthday! Send them some cheers to remind them they're 1 year older! 🎉")
        except Exception as e:
            print(f"Error checking birthdays: {e}")
        await asyncio.sleep(86400)  # Check once every 24 hours