from darrcord.connection import Connection
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env'))


class Config(object):
    DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY')

    LOG_LEVEL = os.environ.get('LOG_LEVEL')
    LOG_FOLDER = os.environ.get('LOG_FOLDER')
    LOG_NAME = os.environ.get('LOG_NAME')

    SONARR_ENABLED = os.environ.get('SONARR_ENABLED')
    SONARR_CONNECTION = Connection(os.environ.get('SONARR_URI'),os.environ.get('SONARR_API_KEY'))
    SONARR_ROOT_FOLDER_PATH = os.environ.get('SONARR_ROOT_FOLDER_PATH')
    SONARR_ROOT_ANIME_PATH = os.environ.get('SONARR_ROOT_ANIME_PATH')
    SONARR_CHANNELS= os.environ.get('SONARR_CHANNELS').split(';')

    RADARR_ENABLED=os.environ.get('RADARR_ENABLED')
    RADARR_CONNECTION = Connection(os.environ.get('RADARR_URI'),os.environ.get('RADARR_API_KEY'))
    RADARR_ROOT_FOLDER_PATH=os.environ.get('RADARR_ROOT_FOLDER_PATH')
    RADARR_CHANNELS=os.environ.get('RADARR_CHANNELS').split(';')
