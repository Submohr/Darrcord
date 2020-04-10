import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from config import Config

logger = logging.getLogger("Rotating Log")
logger.setLevel(Config.LOG_LEVEL or "DEBUG")

handler = None

if Config.LOG_FOLDER and Config.LOG_NAME:
    try:
        os.makedirs(Config.LOG_FOLDER, exist_ok=True)
        handler = RotatingFileHandler("/".join([Config.LOG_FOLDER, Config.LOG_NAME]), maxBytes=102400, backupCount=10)
    except Exception as e:
        print(e)

if not handler:
    handler = logging.StreamHandler(sys.stdout)

handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
logger.addHandler(handler)
logger.info(f"Logger initialized with {handler}.")


from darrcord import disc
if Config.SONARR_ENABLED:
    from darrcord import sonarr
if Config.RADARR_ENABLED:
    from darrcord import radarr
