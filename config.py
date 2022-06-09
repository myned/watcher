import toml
import hikari


# Hikari activity type
# https://www.hikari-py.dev/hikari/presences.html#hikari.presences.ActivityType
ACTIVITY = hikari.ActivityType.WATCHING
# Default bot configuration
CONFIG = """\
client = 0 # bot application id
token = "" # bot token
activity = "you" # bot status
db = "watcher.db" # sqlite3 db filepath
guild = 0 # guild id to watch
active = 0 # active role id
inactive = 0 # inactive role id
duration = 0 # time in seconds before considered inactive
"""

# Load or create config.toml
try:
    config = toml.load("config.toml")
except FileNotFoundError:
    with open("config.toml", "w") as f:
        f.write(CONFIG)
        print("config.toml created with default values. Restart when modified")
        exit()
