from decouple import RepositoryIni, Config

config = Config(RepositoryIni("settings.ini"))

CLIENT_ID               = config("CLIENT_ID")
CLIENT_SECRET           = config("CLIENT_SECRET")
SPOTIFY_REDIRECT_URI    = config("SPOTIFY_REDIRECT_URI")
DB_CONNSTR              = config("DB_CONNSTR")

