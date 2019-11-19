import darrcord
from config import Config

client = darrcord.disc.get_client()
DISCORD_TOKEN = Config.DISCORD_TOKEN
client.run(DISCORD_TOKEN)
