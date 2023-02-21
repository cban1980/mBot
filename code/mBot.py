import os
from nextcord import Intents
import nextcord
from nextcord.ext import commands
import logging
from dotenv import load_dotenv
import random
import requests
from bs4 import BeautifulSoup as bs


# Set up basic logging.

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
list_guild_ids = os.getenv("GUILD_ID")

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

# Bofh function to use for Bot activity upon login.
def bofh():
    """Return random bofh quote"""
    url_data = requests.get('http://pages.cs.wisc.edu/~ballard/bofh/excuses').text
    soup = bs(url_data, 'html.parser')
    for line in soup:
        soppa = line.splitlines()
        soppa = random.choice(soppa)
    return soppa


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(activity=nextcord.Game(name=bofh()))

# Some bot commands for handling loading and unloading of cogs.

class CogLoads(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    async def cog_check(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("You lack permissions for this command.")
            return False
        return True

    @bot.slash_command(description="Load cog.")
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

    @bot.slash_command(description="Unload cog.")
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

    @bot.slash_command(description="Reload cogs.")
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
