from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
PGUSER = env.str('PGUSER')
PGPASSWORD = env.str('PGPASSWORD')
HOST = env.str('HOST')
PRIVATE_CHANNEL_ID = env.str('PRIVATE_CHANNEL_ID')
OFFERS_CHANNEL_ID = env.str('OFFERS_CHANNEL_ID')
BINANCE_API_KEY = env.str('BINANCE_API_KEY')
BINANCE_SECRET_KEY = env.str('BINANCE_SECRET_KEY')
ADMINS_ID = env.str('ADMINS_ID').split(',')
SITE_TOKEN = env.str('SITE_TOKEN')
