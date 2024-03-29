"""Main bot function and cog handling."""
import logging
import random
import os
from nextcord import Intents
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import requests
from bs4 import BeautifulSoup as bs


# Set up basic logging.

logging.basicConfig(level=logging.ERROR)

with open("../config/token", "r", encoding="utf-8") as file:
    for line in file:
        if line.startswith("DISCORD_TOKEN="):
            TOKEN = line[len("DISCORD_TOKEN="):].strip()
            break

intents = nextcord.Intents.default()
intents.message_content = True
intents.typing = True
intents.presences = True
bot = commands.Bot(command_prefix='!', intents=intents)
script_dir = os.path.dirname(os.path.abspath(__file__))

@bot.event
async def on_ready():
    """Prints bot name and ID when bot is ready."""
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(activity=nextcord.Game(name=bofh()))

# Some bot commands for handling loading and unloading of cogs.
# These commands are pretty much self explainatory.

initial_extensions = []
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        cog_name = f'\033[94m{filename[:-3]}\033[0m'
        print(f'Loaded Cog: {cog_name}')
        bot.load_extension(f'cogs.{filename[:-3]}')

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

def bofh():
    """Return random bofh quote"""
    url_data = requests.get('http://pages.cs.wisc.edu/~ballard/bofh/excuses', timeout=10).text
    soup = bs(url_data, 'html.parser')
    for line in soup:
        soppa = line.splitlines()
        soppa = random.choice(soppa)
    return soppa

class Mbot(commands.Cog):
    """Cog for handling loading and unloading of cogs."""
    def __init__(self, bot):
        self.client = bot

    def cog_check(self, ctx):
        """Check if user is admin."""
        if not ctx.author.guild_permissions.administrator:
            ctx.send("You lack permissions for this command.")
            return False
        return True

    @bot.slash_command(description="Load cog.")
    async def loadcog(ctx, extension):
        """Load cog."""
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
        """Unload cog."""
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
        """Reload cog."""
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
        """List currently loaded cogs."""
        loaded_cogs = ", ".join(bot.extensions.keys())
        await interaction.send(f"⚙️ Loaded cogs: {loaded_cogs} ⚙️")

bot.run(TOKEN)
    