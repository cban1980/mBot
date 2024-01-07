# Name: info.py
# Description: Information functions/methods and slash commands.

import feedparser
import json
import os
from nextcord.ext import tasks, commands
import nextcord
import discord
from bs4 import BeautifulSoup

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rss_feeds = self.load_rss_feeds('../config/rssfeeds.conf')
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.latest_posts_file = os.path.join(script_dir, '../../config/latest_posts.json')
        if os.path.exists(self.latest_posts_file):
            with open(self.latest_posts_file, 'r') as f:
                self.latest_posts = json.load(f)
        else:
            self.latest_posts = {}

        # Add any new feeds to latest_posts
        for feed in self.rss_feeds:
            if feed not in self.latest_posts:
                self.latest_posts[feed] = None

        self.check_feed.start()

    def load_rss_feeds(self, file_path):
        rss_feeds = {}
        with open(file_path, 'r') as f:
            for line in f:
                if ' ' not in line:
                    continue
                feed_name, feed_url = line.strip().split(' ', 1)
                rss_feeds[feed_name] = feed_url
        return rss_feeds

    def cog_unload(self):
        self.check_feed.cancel()

    @tasks.loop(minutes=1.0)  # Checks every 10 minutes, adjust as needed
    async def check_feed(self):
        for feed_name, feed_url in self.rss_feeds.items():
            feed = feedparser.parse(feed_url)
            most_recent_entry = feed.entries[0]

            if self.latest_posts[feed_name] == most_recent_entry.id:
                continue

            self.latest_posts[feed_name] = most_recent_entry.id
            with open('../data/latest_posts.json', 'w') as f:
                json.dump(self.latest_posts, f)

            channel = nextcord.utils.get(self.bot.get_all_channels(), name='tech-nyheter')

            if channel:
                soup = BeautifulSoup(most_recent_entry.summary, 'html.parser')
                clean_summary = soup.get_text()
                embed = discord.Embed(title=most_recent_entry.title, description=clean_summary, url=most_recent_entry.link)
                embed.set_author(name=feed_name)  # Set the name of the RSS feed as the author of the embed

                if 'media_content' in most_recent_entry:
                    embed.set_image(url=most_recent_entry.media_content[0]['url'])

                await channel.send(embed=embed)

    @check_feed.before_loop
    async def before_check_feed(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(info(bot))