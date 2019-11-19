from config import Config
from darrcord import logger
from darrcord import api

conn = Config.SONARR_CONNECTION


def req_series_lookup(name=None,id=0):
    if name is None and id==0:
        return
    URI = "series/lookup"
    if name:
        params = {"term":name}
    else:
        params = {"term":f"tvdb:{id}"}
    return api.req_item_lookup(conn, URI, params)


def req_series_request(id):
    look = req_series_lookup(id=id)
    try:
        lookup=look["json"][0]
    except IndexError:
        return {"code":600, "json":[{"message":f"Could not find series with id {id}"}]}

    if look['code']>=400:
        return look

    body = {'title': lookup['title'], 'tvdbId': id, 'profileId': 1, 'titleSlug': lookup['titleSlug'],
            'images': lookup['images'], 'seasons': lookup['seasons'], 'seasonFolder': True,
            'addOptions': {"ignoreEpisodesWithFiles": False,
                           "ignoreEpisodesWithoutFiles": False,
                           "searchForMissingEpisodes": True
                           }}

    if 'Anime' in lookup['genres']:
        body['rootFolderPath'] = Config.SONARR_ROOT_ANIME_PATH
    else:
        body['rootFolderPath'] = Config.SONARR_ROOT_FOLDER_PATH

    URI = "series"
    return api.req_item(conn,URI,body)

