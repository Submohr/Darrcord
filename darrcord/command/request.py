import discord
import re
from config import Config
from darrcord import sonarr
from darrcord import radarr
from darrcord import logger

nonce = 202260

def request_sonarr_series(series, title="series"):
    id = int(series)
    son_resp = sonarr.req_series_request(id)
    code = son_resp["code"]
    resp = son_resp["json"]
    if not resp:
        ret = {'content': f"Error adding {title}.  No error message.  Sorry."}
    elif code >= 200 and code < 400:
        ret = {'content': f"Successfully requested {resp[0]['title']}: {sonarr.tvdb_url}{id}"}
    else:
        ret = {'content': f"Error adding {title}.  Error message is: {resp[0]['errorMessage']}."}
    return ret

def request_radarr_movie(movie, title="movie"):
    id = int(movie)
    son_resp = radarr.req_movie_request(id)
    code = son_resp["code"]
    resp = son_resp["json"]
    if not resp:
        ret = {'content': f"Error adding {title}.  No error message.  Sorry."}
    elif code >= 200 and code < 400:
        ret = {'content': f"Successfully requested {resp[0]['title']}: {radarr.tmdb_url}{id}"}
    else:
        ret = {'content': f"Error adding {title}.  Error message is: {resp[0]['errorMessage']}."}
    return ret

async def handle_message(text, message, **kwargs):
    """ Handles messages in the format tmdb:12345 or tvdb:12345, and ignores anything else.
    If the message is received on a channel configured specially for radarr or sonarr, the
    prefix can be omitted. """

    radarr_regex = r'tmdb:(\d+)'
    if match := re.fullmatch(radarr_regex, text):
        return request_radarr_movie(match.group(1), **kwargs)

    sonarr_regex = r'tvdb:(\d+)'
    if match := re.fullmatch(sonarr_regex, text):
        return request_sonarr_series(match.group(1), **kwargs)

async def handle_reaction(reaction, user):
    pass
