# Name: info.py
"""Cog relating to information commands and functions."""

import json
import os
import feedparser
import nextcord
from nextcord.ext import tasks, commands
from nextcord import Interaction
from bs4 import BeautifulSoup

rss_feeds_file = '../config/rssfeeds.conf'
latest_posts_file = '../data/latest_posts.json'

class Info(commands.Cog):
    """Information commands and functions."""
    def __init__(self, bot):
        """Initialize the cog."""
        self.bot = bot
        self.rss_feeds = self.load_rss_feeds(rss_feeds_file)
        self.latest_posts_file = latest_posts_file
        if os.path.exists(self.latest_posts_file) and os.path.getsize(self.latest_posts_file) > 0:
            with open(self.latest_posts_file, 'r', encoding="utf-8") as f:
                self.latest_posts = json.load(f)
        else:
            self.latest_posts = {}

        # Add any new feeds to latest_posts
        for feed in self.rss_feeds:
            if feed not in self.latest_posts:
                self.latest_posts[feed] = None

        self.check_feed.start()

    def load_rss_feeds(self, file_path):
        """Load RSS feeds from a file."""
        rss_feeds = {}
        with open(file_path, 'r', encoding="utf-8") as f:
            for line in f:
                if ' ' not in line:
                    continue
                feed_name, feed_url = line.strip().split(' ', 1)
                rss_feeds[feed_name] = feed_url
        return rss_feeds

    def cog_unload(self):
        """Stop the background task when the cog is unloaded."""
        self.check_feed.cancel()


    @tasks.loop(minutes=1.0)  # Checks every 1 minutes, adjust as needed
    async def check_feed(self):
        """Check for new posts in the RSS feeds."""
        for feed_name, feed_url in self.rss_feeds.items():
            feed = feedparser.parse(feed_url)
            most_recent_entry = feed.entries[0]
            if (feed_name in self.latest_posts and
            self.latest_posts[feed_name] == most_recent_entry.id):
                continue

            self.latest_posts[feed_name] = most_recent_entry.id
            with open(self.latest_posts_file, 'w', encoding="utf-8") as f:
                json.dump(self.latest_posts, f)

            channel = nextcord.utils.get(self.bot.get_all_channels(), name='tech-nyheter')

            if channel:
                if hasattr(most_recent_entry, 'summary'):
                    soup = BeautifulSoup(most_recent_entry.summary, 'html.parser')
                    clean_summary = soup.get_text()
                else:
                    clean_summary = ''
                embed = nextcord.Embed(title=most_recent_entry.title,
                                        description=clean_summary, url=most_recent_entry.link)
                embed.set_author(name=feed_name)

                if 'media_content' in most_recent_entry:
                    embed.set_image(url=most_recent_entry.media_content[0]['url'])

                if 'tags' in most_recent_entry:
                    categories = ', '.join(tag['term'] for tag in most_recent_entry.tags)
                    embed.add_field(name='Categories', value=categories, inline=False)

                await channel.send(embed=embed)

    @nextcord.slash_command(description="Add an RSS feed to the bot.")
    async def add_feed(self, ctx: Interaction, name: str, url: str):
        """Add an RSS feed to the bot."""
        if ctx.user.guild_permissions.administrator:
            if name in self.rss_feeds:
                await ctx.send(f"Feed {name} already exists.")
            else:
                with open(rss_feeds_file, 'a', encoding="utf-8") as f:
                    f.write(f"\n{name} {url}\n")
                self.rss_feeds[name] = url
                await ctx.send(f"Feed {name} added.")
        else:
            await ctx.send("You lack permissions for this command.")

    @nextcord.slash_command(description="Remove an RSS feed from the bot.")
    async def remove_feed(self, ctx: Interaction, name: str):
        """Remove an RSS feed from the bot."""
        if ctx.user.guild_permissions.administrator:
            if name in self.rss_feeds:
                with open(rss_feeds_file, 'r', encoding="utf-8") as f:
                    lines = f.readlines()
                with open(rss_feeds_file, 'w', encoding="utf-8") as f:
                    for line in lines:
                        if name not in line:
                            f.write(line)
                del self.rss_feeds[name]
                await ctx.send(f"Feed {name} removed.")
            else:
                await ctx.send(f"Feed {name} does not exist.")
        else:
            await ctx.send("You lack permissions for this command.")

    @nextcord.slash_command(description="List all RSS feeds.")
    async def list_feeds(self, ctx: Interaction):
        """List all RSS feeds."""
        if ctx.user.guild_permissions.administrator:
            embed = nextcord.Embed(title="RSS feeds", color=0x00ff00)
            for feed_name, feed_url in self.rss_feeds.items():
                embed.add_field(name=feed_name, value=feed_url, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("You lack permissions for this command.")

    @check_feed.before_loop
    async def before_check_feed(self):
        """Wait until the bot is ready."""
        await self.bot.wait_until_ready()

def setup(bot):
    """Add the cog to the bot."""
    bot.add_cog(Info(bot))
