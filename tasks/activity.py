import datetime as dt
import hikari
import lightbulb
from lightbulb.ext import tasks

import config as c


plugin = lightbulb.Plugin("activity")


# Check every minute if inactive
@tasks.task(s=60)
async def check_activity():
    for author_id, timestamp in c.db.items():
        if dt.datetime.now(dt.timezone.utc) - timestamp >= dt.timedelta(seconds=c.config["duration"]):
            try:
                member = plugin.bot.cache.get_member(
                    c.config["guild"], author_id
                ) or await plugin.bot.rest.fetch_member(c.config["guild"], author_id)

                if c.config["active"] and c.config["active"] in member.role_ids:
                    await member.remove_role(c.config["active"])
                if c.config["inactive"] and c.config["inactive"] not in member.role_ids:
                    await member.add_role(c.config["inactive"])
            except hikari.NotFoundError:
                print(f"Member {author_id} not found. Deleting entry...")
                del c.db[author_id]


# Listener for bot ready
@plugin.listener(hikari.StartedEvent)
async def on_ready(event):
    check_activity.start()


# Listener for guild messages
@plugin.listener(hikari.GuildMessageCreateEvent)
async def on_message(event):
    if event.is_bot or event.guild_id != c.config["guild"] or c.config["exclude"] in event.member.role_ids:
        return

    c.db[event.author_id] = dt.datetime.now(dt.timezone.utc)  # or event.message.timestamp

    if c.config["active"] and c.config["active"] not in event.member.role_ids:
        await event.member.add_role(c.config["active"])
    if c.config["inactive"] and c.config["inactive"] in event.member.role_ids:
        await event.member.remove_role(c.config["inactive"])


# Listener for voice state
@plugin.listener(hikari.VoiceStateUpdateEvent)
async def on_voice(event):
    if (
        event.state.member.is_bot
        or event.guild_id != c.config["guild"]
        or c.config["exclude"] in event.state.member.role_ids
    ):
        return

    c.db[event.state.user_id] = dt.datetime.now(dt.timezone.utc)

    if c.config["active"] and c.config["active"] not in event.state.member.role_ids:
        await event.state.member.add_role(c.config["active"])
    if c.config["inactive"] and c.config["inactive"] in event.state.member.role_ids:
        await event.state.member.remove_role(c.config["inactive"])


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
