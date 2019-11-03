import discord
import darrcord.radarr
import darrcord.sonarr
import config

TOKEN = config.DISCORD_TOKEN
client = discord.Client()
client.run(TOKEN)

@client.event
async def on_message(message):
    # we do not want the bot to look at its own messages
    if message.author == client.user:
        return
