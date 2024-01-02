# Name: moderation.py
# Description: Moderation slash commands for mBot.

import nextcord
from nextcord.ext import commands
from nextcord import Interaction

class moderation(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    # Create the text channel #moderation if it doesnt exist.
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            channel = nextcord.utils.get(guild.channels, name="moderation")
            if not channel:
                overwrites = {
                    guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                    nextcord.utils.get(guild.roles, name="Admin"): nextcord.PermissionOverwrite(read_messages=True)
                }
                await guild.create_text_channel("moderation", overwrites=overwrites)

    
    # Slash command that will delete all posts by users on the server.
    @nextcord.slash_command(description="Delete posts by a user.")
    async def user_purge(self, ctx: Interaction, user: nextcord.Member, limit: str, channel: nextcord.TextChannel = None):
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
    
    # A listener that will look in all messages sent in the server. If the message contains a link, it will post in  the server chanel #moderation who sent the link, at what time, and the link itself.
    # This will be sent as an embed.
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if message.channel.name != "moderation":
                if "http" in message.content or message.content.startswith("www"):
                    moderation_channel = nextcord.utils.get(message.guild.channels, name="moderation")
                    if moderation_channel:
                        embed = nextcord.Embed(title="Link posted", description=f"User {message.author.mention} posted a link in {message.channel.mention} at {message.created_at}.", color=0x00ff00)
                        embed.add_field(name="Link", value=message.content, inline=False)
                        
                        # Add interaction button for "Go to Message".
                        go_to_message_button = nextcord.ui.Button(style=nextcord.ButtonStyle.link, label="Go to Message", url=message.jump_url)
                        
                        view = nextcord.ui.View()
                        view.add_item(go_to_message_button)
                        
                        await moderation_channel.send(embed=embed, view=view)
                        
def setup(bot):
    bot.add_cog(moderation(bot))