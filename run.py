import os
import hikari
import lightbulb
import miru
from lightbulb.ext import tasks

import config as c


# Unix optimizations
# https://github.com/hikari-py/hikari#uvloop
if os.name != "nt":
    import uvloop

    uvloop.install()

intents = (
    hikari.Intents.GUILDS  # limbo
    | hikari.Intents.GUILD_MEMBERS  # limbo
    | hikari.Intents.GUILD_MESSAGES  # activity
    | hikari.Intents.GUILD_MESSAGE_TYPING  # activity
    | hikari.Intents.GUILD_VOICE_STATES  # activity
)
bot = lightbulb.BotApp(token=c.config["token"], intents=intents)


# Listener for global exceptions
@bot.listen(hikari.ExceptionEvent)
async def on_error(event):
    exception = event.exception.__cause__ or event.exception

    await (await bot.rest.fetch_application()).owner.send(f"```❗ {type(exception).__name__}: {exception}```")

    raise event.exception


miru.install(bot)
tasks.load(bot)
bot.load_extensions_from("commands", "tasks")
bot.run(activity=hikari.Activity(name=c.config["activity"], type=c.ACTIVITY) if c.config["activity"] else None)
