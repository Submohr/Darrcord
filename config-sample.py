from darrcord.connection import Connection
import logging


class Config(object):
    DISCORD_TOKEN='discordtokenhere'

    LOG_LEVEL = logging.INFO
    LOG_FOLDER = 'logs'
    LOG_NAME = 'darrcord.log'

    SONARR_ENABLED=True
    SONARR_CONNECTION = Connection('https://sonarr_api_uri_here_endswith/api/','sonarr_api_key_here')
    SONARR_ROOT_FOLDER_PATH = "sonarr_root_folder_path"
    SONARR_ROOT_ANIME_PATH = "sonarr_anime_folder_path_lol"

    RADARR_ENABLED=True
    RADARR_CONNECTION = Connection('https://radarr_api_uri_here_endswith/api/','radarr_api_key_here')
    RADARR_ROOT_FOLDER_PATH="radarr_root_folder_path"

    SONARR_CHANNELS=["sonarr","tv"]
    RADARR_CHANNELS=["radarr","movies"]

