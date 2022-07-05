import hikari
import lightbulb
from miru.ext import nav

import config as c
from tools import components


plugin = lightbulb.Plugin("info", default_enabled_guilds=c.config["guild"])


# Get list of inactive members
@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_GUILD))
@lightbulb.command("inactive", "List inactive members", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def inactive(context):
    def build(index, content):
        return hikari.Embed(
            title="Inactive", description=content, color=context.get_guild().get_my_member().get_top_role().color
        ).set_footer(f"{len(inactive)} members")

    inactive = {
        snowflake: member
        for snowflake, member in sorted(
            context.get_guild().get_members().items(), key=lambda item: item[1].display_name
        )
        if snowflake not in c.db
    }

    paginator = lightbulb.utils.EmbedPaginator()
    paginator.set_embed_factory(build)
    for snowflake, member in inactive.items():
        paginator.add_line(f"{member.mention} {snowflake}")
    pages = [page for page in paginator.build_pages()]

    if len(pages) > 1:
        navigator = nav.NavigatorView(
            pages=pages,
            buttons=[components.Back(), components.Forward()],
            timeout=600,
        )
        await navigator.send(context.interaction, ephemeral=True)
    else:
        await context.respond(pages[0])


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)