import asyncio
import aiohttp
from config import Config
from darrcord import logger

API_HOST = 'https://api.themoviedb.org/3'
movie_url = 'https://www.themoviedb.org/movie/'
tv_url = 'https://www.themoviedb.org/tv/'

async def tmdb_get(endpoint, **kwargs):
    url = API_HOST + endpoint
    params = dict(kwargs, api_key=Config.TMDB_API_KEY)
    logger.debug(f"TMDB url {url} params {params}")

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return (resp.status, await resp.json())

async def search_multi(search_terms, media_types):
    status, json = await tmdb_get('/search/multi', query=search_terms)
    if status != 200:
        logger.error(f"Got error response from TMDB {json}")
        return []

    logger.debug(f"TMDB search found {json['total_results']} results")

    def process(entry):
        date = entry.get('release_date') or entry.get('first_air_date') or ''
        entry['year'] = date.split('-')[0]
        entry['title'] = entry.get('title') or entry.get('name')
        return entry

    return [ process(entry) for entry in json['results'] if entry['media_type'] in media_types ]

async def tmdb_to_tvdb(tmdb_id):
    status, json = await tmdb_get(f'/tv/{tmdb_id}/external_ids')
    if status != 200:
        logger.error(f"Got error response from TMDB {json}")
        return None

    return json['tvdb_id']
