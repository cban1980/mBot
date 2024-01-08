# Name: moderation.py
"""Cog relating to moderation commands and functions."""

import nextcord
from nextcord.ext import commands
from nextcord import Interaction

class moderation(commands.Cog):
    """Moderation commands and functions."""
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Create the text channel"""
        for guild in self.bot.guilds:
            channel = nextcord.utils.get(guild.channels, name="moderation")
            if not channel:
                overwrites = {
        guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
        nextcord.utils.get(guild.roles, name="Admin"):
            nextcord.PermissionOverwrite(read_messages=True)
    }
                await guild.create_text_channel("moderation", overwrites=overwrites)


    @nextcord.slash_command(description="Delete posts by a user.")
    async def message_purge(
        self,
        ctx: Interaction,
        user: nextcord.Member,
        limit: str,
        channel: nextcord.TextChannel = None
    ):
        """Delete posts by a user."""
        if ctx.user.guild_permissions.administrator:
            if limit.lower() == 'all':
                channel = ctx.channel if channel is None else channel
                await channel.purge(check=lambda m: m.author == user)
                await ctx.send(f"Deleted all posts by {user.mention} in {channel.name}.")
            else:
                limit = int(limit)
                channel = ctx.channel if channel is None else channel
                await channel.purge(limit=limit, check=lambda m: m.author == user)
                await ctx.send(f"Deleted last {limit} posts by {user.mention} in {channel.name}.")
        else:
            await ctx.send("You lack permissions for this command.")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Check if message contains a link, and post it in #moderation."""
        if not message.author.bot:
            if message.channel.name != "moderation":
                if "http" in message.content or message.content.startswith("www"):
                    moderation_channel = nextcord.utils.get(
                        message.guild.channels,
                        name="moderation"
                    )
                    if moderation_channel:
                        embed = nextcord.Embed(
                            title="Link posted",
                            description=(
                                f"User {message.author.mention} posted a link in "
                                f"{message.channel.mention} at {message.created_at}."
                            ),
                            color=0x00ff00
                        )
                        embed.add_field(name="Link", value=message.content, inline=False)
                        # Add interaction button for "Go to Message".
                        go_to_message_button = nextcord.ui.Button(
                            style=nextcord.ButtonStyle.link,
                            label="Go to Message",
                            url=message.jump_url
                        )
                        view = nextcord.ui.View()
                        view.add_item(go_to_message_button)
                        await moderation_channel.send(embed=embed, view=view)

def setup(bot):
    """Add the cog to the bot."""
    bot.add_cog(moderation(bot))
