import psycopg2 as psy
from config_pack import config
from config_pack import password as pw

def create_connection():
    connection = psy.connect(database=config.database(), user=config.user(), password= pw.password(), host=config.host(), port=config.port())
    cursor = connection.cursor()

