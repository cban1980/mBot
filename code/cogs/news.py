# Name: news.py
# Description: cog for handing news updates, webhooks and rss feeds.

import nextcord
from nextcord.ext import tasks, commands
from nextcord import Interaction
import feedparser
import json

class news(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

# dict of rss feeds to check for updates.
# dict of rss feeds to check for updates.
rss_feeds = { "IDG-opensource": "https://computersweden.idg.se/rss/%C3%B6ppen+k%C3%A4llkod", "Slashdot-Linux": "https://rss.slashdot.org/Slashdot/slashdotLinux", "CNN-Technology": "http://rss.cnn.com/rss/edition_technology.rss" }

# nextcord function that will run check_rss_feeds() every 10 minutes. and if a new rss feed is found, it will post it in the channel #tech-nyheter.
# This will be sent as an embed.
@tasks.loop(minutes=1)
async def rss_feed_check(self):
    await self.bot.wait_until_ready()
    channel = nextcord.utils.get(self.bot.get_all_channels(), name="tech-nyheter")
    if channel:
        for feed in rss_feeds:
            feed = feedparser.parse(rss_feeds[feed])
            for entry in feed.entries:
                if entry.published_parsed > feed.feed.published_parsed:
                    embed = nextcord.Embed(title=entry.title, description=entry.summary, color=0x00ff00)
                    embed.add_field(name="Link", value=entry.link, inline=False)
                    await channel.send(embed=embed)
def setup(bot):
    bot.add_cog(news(bot))