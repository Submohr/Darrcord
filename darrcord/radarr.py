from config import Config
from darrcord import logger
from darrcord import api

conn = Config.RADARR_CONNECTION
tmdb_url = 'https://www.themoviedb.org/movie/'

def req_movie_lookup(name=None,tmdbId=0,imdbIdStr=None,imdbId=0):
    if name is None and tmdbId==0 and imdbIdStr is None and imdbId == 0:
        return
    URI = "movie/lookup"
    if name:
        params = {"term":name}
    elif tmdbId > 0:
        URI = URI + "/tmdb"
        params = {"tmdbId":f"{tmdbId}"}
    else:
        URI = URI + "/imdb"
        if imdbIdStr is not None:
            params = {"imdbId":imdbIdStr}
        else:
            params = {"imdbId":f"tt{imdbId}"}
    logger.info(f"URI: {URI}, params: {params}")
    return api.req_item_lookup(conn, URI, params)


#req_movie_lookup works with imdbids and stuff but we're only gonna implement tmdbId for now
def req_movie_request(tmdbId):
    logger.info(f"in req_movie_request: tmdbId = {tmdbId}")
    look = req_movie_lookup(tmdbId=tmdbId)
    logger.info(f"in req_movie_request: look =  {look}")
    try:
        lookup=look["json"][0]
    except IndexError:
        return {"code":600, "json":[{"message":f"Could not find movie with id {tmdbId}"}]}

    if look['code']>=400:
        return look

    body = {'title': lookup['title'], 'tmdbId': tmdbId, 'qualityProfileId': 1, 'titleSlug': lookup['titleSlug'],
            'images': lookup['images'], 'year': lookup['year'], "rootFolderPath": Config.RADARR_ROOT_FOLDER_PATH,
            "monitored":True, 'addOptions': {"searchForMovie": True}}

    URI = "movie"
    return api.req_item(conn,URI,body)

