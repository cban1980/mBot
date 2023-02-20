import os
from nextcord import Intents
import nextcord
from nextcord.ext import commands
import logging

# Set up basic logging.

logging.basicConfig(level=logging.INFO)
list_guild_ids = 1049804249204264972  

intents = nextcord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

initial_extensions = []
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        print(f'Loaded Cog: {filename[:-3]}')
        bot.load_extension(f'cogs.{filename[:-3]}')

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

TOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# Some bot commands for handling loading and unloading of cogs.

class CogLoads(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @bot.slash_command(description="Load cog.", guild_ids=[list_guild_ids])
    async def loadcog(ctx, extension):
        try:
            bot.load_extension(f"cogs.{extension}")
            await ctx.send(f"⚙️ Loaded extension: {extension} ✅")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"⚙️ Extension {extension} was not loaded. ❌")
        except commands.ExtensionNotFound:
            await ctx.send(f"⚙️ Extension {extension} was not found. ❌")
        except Exception as e:
            await ctx.send(f"⚙️ An error occurred while unloading extension {extension}: {e} ❌")

    @bot.slash_command(description="Unload cog.", guild_ids=[list_guild_ids])
    async def unloadcog(ctx, extension):
        try:
            bot.unload_extension(f"cogs.{extension}")
            await ctx.send(f"⚙️ Unloaded extension: {extension} ✅")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"⚙️ Extension {extension} was not loaded. ❌")
        except commands.ExtensionNotFound:
            await ctx.send(f"⚙️ Extension {extension} was not found. ❌")
        except Exception as e:
            await ctx.send(f"⚙️ An error occurred while unloading extension {extension}: {e} ❌")

    @bot.slash_command(description="Reload cogs.", guild_ids=[list_guild_ids])
    async def reloadcogs(ctx, extension):
        try:
            bot.reload_extension(f"cogs.{extension}")
            await ctx.send(f"⚙️ Reloaded extension: {extension} ✅")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"-⚙️ Extension {extension} was not loaded. ❌")
        except commands.ExtensionNotFound:
            await ctx.send(f"⚙️ Extension {extension} was not found. ❌")
        except Exception as e:
            await ctx.send(f"⚙️ An error occurred while unloading extension {extension}: {e} ❌")
    
    @bot.slash_command(name="listcogs", description="List currently loaded cogs.")
    async def listcogs(interaction: nextcord.Interaction):
        loaded_cogs = ", ".join(bot.extensions.keys())
        await interaction.send(f"⚙️ Loaded cogs: {loaded_cogs} ⚙️")



bot.run(TOKEN)
