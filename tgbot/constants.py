from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
DB_HOST = env.str("DB_HOST")
DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DB_DATABASE = env.str("DB_DATABASE")
DB_URL = env.str('DB_URL')
DB_LITE = env.str('DB_LITE')
