import datetime as dt
import hikari
import lightbulb
from lightbulb.ext import tasks

import config as c


plugin = lightbulb.Plugin("activity")


# Check every minute if inactive (or config duration if under 60 secs)
@tasks.task(s=60 if c.config["duration"] >= 60 else c.config["duration"])
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
                if c.config["exclude"] in member.role_ids:
                    del c.db[author_id]
                    continue

                # Enforce activity roles
                if c.config["active"] in member.role_ids:
                    await member.remove_role(c.config["active"])
                if c.config["inactive"] not in member.role_ids:
                    await member.add_role(c.config["inactive"])
            # Delete member from db if not found
            except hikari.NotFoundError:
                del c.db[author_id]


# Listener for bot ready
@plugin.listener(hikari.StartedEvent)
async def on_ready(event):
    check_activity.start()


# Check activity and update timestamp
async def update_activity(event, member):
    # Exclude other guilds
    if event.guild_id != c.config["guild"]:
        return

    # Exclude and remove activity roles from excluded role
    if c.config["exclude"] in member.role_ids:
        if c.config["active"] in member.role_ids:
            await member.remove_role(c.config["active"])
        if c.config["inactive"] in member.role_ids:
            await member.remove_role(c.config["inactive"])
        return

    # Insert current timestamp into db
    c.db[member.id] = dt.datetime.now(dt.timezone.utc)

    # Toggle activity roles
    if c.config["active"] not in member.role_ids:
        await member.add_role(c.config["active"])
    if c.config["inactive"] in member.role_ids:
        await member.remove_role(c.config["inactive"])


# Listener for guild messages
@plugin.listener(hikari.GuildMessageCreateEvent)
async def on_message(event):
    # Exclude bots and webhooks
    if event.is_human:
        await update_activity(event, event.member)


# Listener for guild typing
@plugin.listener(hikari.GuildTypingEvent)
async def on_typing(event):
    # Exclude bots
    if not event.member.is_bot:
        await update_activity(event, event.member)


# Listener for voice state
@plugin.listener(hikari.VoiceStateUpdateEvent)
async def on_voice(event):
    # Exclude bots
    if not event.state.member.is_bot:
        await update_activity(event, event.state.member)


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
