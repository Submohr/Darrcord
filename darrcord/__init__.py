import logging
from logging.handlers import RotatingFileHandler
from config import Config

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)

try:
    handler = RotatingFileHandler("logs/test.log", maxBytes=102400, backupCount=10)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    logger.addHandler(handler)
except:
    logger.addHandler(logging.NullHandler())



from darrcord import disc
if Config.SONARR_ENABLED:
    from darrcord import sonarr
if Config.RADARR_ENABLED:
    from darrcord import radarr