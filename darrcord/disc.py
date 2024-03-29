import asyncio
import discord
from collections import defaultdict
from config import Config
from darrcord import sonarr
from darrcord import radarr
from darrcord import logger
from darrcord.command import request, search

intents = discord.Intents.all()
client = discord.Client(intents=intents)

commands = request, search

def get_client():
    return client

async def send_reply(cmd, channel, reply):
    reply = defaultdict(lambda: None, reply)
    msg = await channel.send(
            content=reply["content"],
            embed=reply["embed"],
            nonce=cmd.nonce)
    if reply["reactions"]:
        # these should run in parallel but adding reactions is still super slow so idk
        await asyncio.gather(*[ msg.add_reaction(emoji) for emoji in reply["reactions"] ])

@client.event
async def on_reaction_add(reaction, user):
    """ When one of our messages is reacted to, this sends the reaction to the command that
    generated the message (identified by the message nonce). """

    try:
        # ignore reactions we send, reactions not on our messages
        if user == client.user or not reaction.message.author == client.user:
            return

        logger.debug(f"Received reaction: {reaction} from {user} on {reaction.message.channel} with nonce {repr(reaction.message.nonce)} and nonce type {type(reaction.message.nonce)}")

        for cmd in commands:
            logger.debug(f"Testing for command {cmd} with nonce {cmd.nonce}: equals = {cmd.nonce == reaction.message.nonce}")
            if cmd.nonce == reaction.message.nonce:
                logger.debug(f"Running cmd.handle_reaction on cmd: {cmd}")
                reply = await cmd.handle_reaction(reaction, user)
                if reply:
                    await send_reply(cmd, reaction.message.channel, reply)
    except (ValueError, Exception) as e:
        logger.exception(e)

@client.event
async def on_message(message):
    """ Sends the message to each command until it finds one that generates a reply. """

    try:
        # we do not want the bot to look at its own messages
        if message.author == client.user:
            return

        text = message.content.strip()
        logger.debug(f"Received message: {text} on {message.channel}")

        reply = None

        for cmd in commands:
            reply = await cmd.handle_message(text, message)
            if reply:
                await send_reply(cmd, message.channel, reply)
                break
    except (ValueError, Exception) as e:
        logger.exception(e)
