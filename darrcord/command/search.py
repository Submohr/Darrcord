import discord
import re
from config import Config
from darrcord import sonarr
from darrcord import radarr
from darrcord import logger
from darrcord.command import request
from toolz import interleave

number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
nonce = 926835

def present_sonarr_choice(json):
    return f"[{json['title']} ({json['year']})]({sonarr.tvdb_url}{json['tvdbId']})"

def present_radarr_choice(json):
    return f"[{json['title']} ({json['year']})]({radarr.tmdb_url}{json['tmdbId']})"

def present_choices(mention, choices):
    lines = [ f"Here's what I found, {mention}. Click a number to select one." ]
    lines.extend([ f"{number_emojis[i]} {choices[i]}" for i in range(len(choices)) ])
    return "\n".join(lines)

def handle_message(text, message):
    """ This will treat any message received as a search string. If the channel the message is
    sent in is set specifically as a sonarr or radarr channel, it will only query that service
    for results, otherwise queries both. """

    search_radarr, search_sonarr = False, False
    if str(message.channel) in Config.SONARR_CHANNELS:
        search_sonarr = True
    if str(message.channel) in Config.RADARR_CHANNELS:
        search_radarr = True
    if not search_radarr and not search_sonarr:
        search_radarr, search_sonarr = True, True

    results = []

    if search_radarr:
        radarr_response = radarr.req_movie_lookup(text)
        results.append([ present_radarr_choice(json) for json in radarr_response["json"] ])

    if search_sonarr:
        sonarr_response = sonarr.req_series_lookup(text)
        results.append([ present_sonarr_choice(json) for json in sonarr_response["json"] ])

    results = list(interleave(results))[:len(number_emojis)]

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
    if not f"<@{user.id}>" in content:
        return

    # I didn't want to store any state in the bot so we are awkwardly parsing all the state
    # we need out of the message
    selected_line = re.search(f"{reaction} ([^\n]*)", content)
    if not selected_line:
        return

    radarr_regex = re.escape(radarr.tmdb_url) + r'(\d+)'
    if radarr_result := re.search(radarr_regex, selected_line.group(0)):
        tmdb = "tmdb:" + radarr_result.group(1)
        logger.info(f"{user} selected movie {tmdb}")
        return request.handle_message(tmdb, None)

    sonarr_regex = re.escape(sonarr.tvdb_url) + r'(\d+)'
    if sonarr_result := re.search(sonarr_regex, selected_line.group(0)):
        tvdb = "tvdb:" + sonarr_result.group(1)
        logger.info(f"{user} selected series {tvdb}")
        return request.handle_message(tvdb, None)