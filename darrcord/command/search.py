import discord
import re
from config import Config
from darrcord import sonarr
from darrcord import tmdb
from darrcord import radarr
from darrcord import logger
from darrcord.command import request
import json

number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
tmdb_movie_url = 'https://www.themoviedb.org/movie/'
tmdb_tv_url = 'https://www.themoviedb.org/tv/'
nonce = 926835

def present_tmdb_movie_choice(json):
    return f"[{json['title']} ({json['year']})]({tmdb_movie_url}{json['id']})"

def present_tmdb_tv_choice(json):
    return f"[{json['title']} ({json['year']})]({tmdb_tv_url}{json['id']})"

def present_tmdb_choice(json):
    if json['media_type'] == 'tv':
        return present_tmdb_tv_choice(json)
    elif json['media_type'] == 'movie':
        return present_tmdb_movie_choice(json)
    raise Exception(f"Unhandled media type in search results: {json['media_type']}")

def present_choices(mention, choices):
    lines = [ f"Here's what I found, {mention}. Click a number to select one." ]
    lines.extend([ f"{number_emojis[i]} {choices[i]}" for i in range(len(choices)) ])
    return "\n".join(lines)

async def handle_message(text, message):
    """ Passes the message as a search term to TMDB, and present the results in a menu the
    user can select from by add a reaction to the message. """

    media_type = []
    if str(message.channel) in Config.SONARR_CHANNELS:
        media_type.append('tv')
    if str(message.channel) in Config.RADARR_CHANNELS:
        media_type.append('movie')
    if not media_type:
        media_type = ['tv', 'movie']

    tmdb_results = await tmdb.search_multi(text, media_type)
    results = [ present_tmdb_choice(result) for result in tmdb_results ]
    results = results[:len(number_emojis)]

    if not results:
        return { "content": "No results." }

    embed = present_choices(message.author.mention, results)
    embed = discord.Embed(description=embed)
    return { "embed": embed, "reactions": number_emojis[:len(results)] }

def handle_reaction(reaction, user):
    """ If the user clicks an emoji on one of our search result messages, this triggers the
    request by firing off a fake message to the request command """

    if not reaction.message.embeds:
        return

    content = reaction.message.embeds[0].description

    # we only care about reactions from whoever performed the search
    if not f"<@{user.id}>" in content and not f"<@!{user.id}>" in content:
        return

    # I didn't want to store any state in the bot so we are awkwardly parsing all the state
    # we need out of the message
    selected_line = re.search(f"{reaction} ([^\n]*)", content)
    if not selected_line:
        return

    radarr_regex = r'\[([^\]]+)\]\(' + re.escape(tmdb_movie_url) + r'(\d+)\)'
    if radarr_result := re.search(radarr_regex, selected_line.group(0)):
        tmdb = "tmdb:" + radarr_result.group(2)
        logger.info(f"{user} selected movie {tmdb}")
        return request.handle_message(tmdb, None, title=radarr_result.group(1))

    sonarr_regex = r'\[([^\]]+)\]\(' + re.escape(tmdb_tv_url) + r'(\d+)\)'
    if sonarr_result := re.search(sonarr_regex, selected_line.group(0)):
        tvdb = "tmdbtv:" + sonarr_result.group(2)
        logger.info(f"{user} selected series {tvdb}")
        return request.handle_message(tvdb, None, title=sonarr_result.group(1))
