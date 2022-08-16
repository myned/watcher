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
        # If time between now and timestamp >= duration
        if dt.datetime.now(dt.timezone.utc) - timestamp >= dt.timedelta(seconds=c.config["duration"]):
            try:
                # Acquire member object
                member = plugin.bot.cache.get_member(
                    c.config["guild"], author_id
                ) or await plugin.bot.rest.fetch_member(c.config["guild"], author_id)

                # Delete member from db if it has excluded role
                if c.config["exclude"] and c.config["exclude"] in member.role_ids:
                    del c.db[author_id]
                    continue

                # Enforce activity roles
                if c.config["active"] and c.config["active"] in member.role_ids:
                    await member.remove_role(c.config["active"])
                if c.config["inactive"] and c.config["inactive"] not in member.role_ids:
                    await member.add_role(c.config["inactive"])
            # Delete member from db if not found
            except hikari.NotFoundError:
                del c.db[author_id]


# Listener for bot ready
@plugin.listener(hikari.StartedEvent)
async def on_ready(event):
    check_activity.start()


# Listener for guild messages
@plugin.listener(hikari.GuildMessageCreateEvent)
async def on_message(event):
    # Exclude bots, unselected guild, and excluded role
    if event.is_bot or event.guild_id != c.config["guild"] or c.config["exclude"] in event.member.role_ids:
        return

    # Insert current timestamp into db
    c.db[event.author_id] = dt.datetime.now(dt.timezone.utc)  # or event.message.timestamp

    # Toggle activity roles
    if c.config["active"] and c.config["active"] not in event.member.role_ids:
        await event.member.add_role(c.config["active"])
    if c.config["inactive"] and c.config["inactive"] in event.member.role_ids:
        await event.member.remove_role(c.config["inactive"])


# Listener for voice state
@plugin.listener(hikari.VoiceStateUpdateEvent)
async def on_voice(event):
    # Exclude bots, unselected guild, and excluded role
    if (
        event.state.member.is_bot
        or event.guild_id != c.config["guild"]
        or c.config["exclude"] in event.state.member.role_ids
    ):
        return

    # Insert current timestamp into db
    c.db[event.state.user_id] = dt.datetime.now(dt.timezone.utc)  # or event.message.timestamp

    # Toggle activity roles
    if c.config["active"] and c.config["active"] not in event.state.member.role_ids:
        await event.state.member.add_role(c.config["active"])
    if c.config["inactive"] and c.config["inactive"] in event.state.member.role_ids:
        await event.state.member.remove_role(c.config["inactive"])


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
