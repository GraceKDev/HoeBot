import logging
import functools
import discord

logger = logging.getLogger(__name__)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

def log_command(func):
    @functools.wraps(func)
    async def wrapper(interaction: discord.Interaction, *args, **kwargs):
        logger.info(
            f"Command /{interaction.command.name} used by {interaction.user} "
            f"(guild={interaction.guild_id})"
        )
        try:
            return await func(interaction, *args, **kwargs)
        except Exception:
            logger.exception(
                f"Error in command /{interaction.command.name}"
            )
            raise

    return wrapper