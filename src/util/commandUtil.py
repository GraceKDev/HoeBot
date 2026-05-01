from datetime import datetime
import json
import logging
async def setBirthday(guild_id, user_id, birthday):
		try:
			with open('src/db.json', 'r') as f:
				data = json.load(f)
			if str(guild_id) not in data:
				data[str(guild_id)] = {}
			if "users" not in data[str(guild_id)]:
				data[str(guild_id)]["users"] = {}
			if str(user_id) not in data[str(guild_id)]["users"]:
				data[str(guild_id)]["users"][str(user_id)] = {}
			data[str(guild_id)]["users"][str(user_id)]["birthday"] = birthday
			with open('src/db.json', 'w') as f:
				json.dump(data, f, indent=4)
		except Exception as e:
			logging.error(f"Error setting birthday: {e}", exc_info=True)
			return False
		return True

async def addGameCompleted(guild_id, user_id, gameForm):
		gameTitle = gameForm.get("title")
		gamePlatform = gameForm.get("platform")
		gamecompletionDate = gameForm.get("completionDate")
		try:
			with open('src/db.json', 'r') as f:
				data = json.load(f)
			if str(guild_id) not in data:
				data[str(guild_id)] = {}
			if "users" not in data[str(guild_id)]:
				data[str(guild_id)]["users"] = {}
			if str(user_id) not in data[str(guild_id)]["users"]:
				data[str(guild_id)]["users"][str(user_id)] = {}
			if "completedGames" not in data[str(guild_id)]["users"][str(user_id)]:
				data[str(guild_id)]["users"][str(user_id)]["completedGames"] = []
			data[str(guild_id)]["users"][str(user_id)]["completedGames"].append({
				"title": gameTitle,
				"platform": gamePlatform,
				"completionDate": gamecompletionDate
			})
			with open('src/db.json', 'w') as f:
				json.dump(data, f, indent=4)
		except Exception as e:
			logging.error(f"Error adding completed game: {e}", exc_info=True)
			return False
		return True

async def getCompletedGames(guild_id, user_id):
		try:
			with open('src/db.json', 'r') as f:
				data = json.load(f)
			if str(guild_id) in data:
				if "users" in data[str(guild_id)]:
					if str(user_id) in data[str(guild_id)]["users"]:
						if "completedGames" in data[str(guild_id)]["users"][str(user_id)]:
							return data[str(guild_id)]["users"][str(user_id)]["completedGames"]
			return []
				
		except Exception as e:
			logging.error(f"Error getting completed games: {e}", exc_info=True)
			return []
				

async def getBirthdays(guild_id):
		try:
			with open('src/db.json', 'r') as f:
				data = json.load(f)
			if str(guild_id) in data:
				if "users" in data[str(guild_id)]:
					return data[str(guild_id)]["users"]
				else:
					return {}
			else:
				return {}
		except Exception as e:
			logging.error(f"Error getting birthdays: {e}", exc_info=True)
			return {}
		
async def getBirthdays(guild_id):
		try:
			with open('src/db.json', 'r') as f:
				data = json.load(f)
			if str(guild_id) in data:
				if "users" in data[str(guild_id)]:
					return data[str(guild_id)]["users"]
				else:
					return {}
			else:
				return {}
		except Exception as e:
			logging.error(f"Error getting birthdays: {e}", exc_info=True)
			return {}
		
async def sortBirthdays(dates):
		try:
			sorted_birthdays = sorted(dates.items(), key=lambda x: x[1]["birthday"])
			return sorted_birthdays
		except Exception as e:
			logging.error(f"Error sorting birthdays: {e}", exc_info=True)
			return dates
		
async def sortGames(games):
    try:
        return sorted(
            games,
            key=lambda g: datetime.strptime(g["completionDate"], "%d/%m/%Y"),
            reverse=True
        )
    except Exception as e:
        logging.error(f"Error sorting games: {e}", exc_info=True)
        return []