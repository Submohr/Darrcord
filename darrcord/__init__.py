import os
import logging
from logging.handlers import RotatingFileHandler
from config import Config

if not os.path.exists(Config.LOG_FOLDER):
    os.mkdir(Config.LOG_FOLDER)

logger = logging.getLogger("Rotating Log")
logger.setLevel(Config.LOG_LEVEL)

try:
    handler = RotatingFileHandler("/".join([Config.LOG_FOLDER, Config.LOG_NAME]), maxBytes=102400, backupCount=10)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    logger.addHandler(handler)
    logger.info("Logger initialized.")
except Exception as e:
    logger.addHandler(logging.NullHandler())
    print(e)
except:
    logger.addHandler(logging.NullHandler())




from darrcord import disc
if Config.SONARR_ENABLED:
    from darrcord import sonarr
if Config.RADARR_ENABLED:
    from darrcord import radarr