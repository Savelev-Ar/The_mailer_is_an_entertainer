from django.core.management import BaseCommand
from configparser import ConfigParser
import psycopg2


def read_config_db(filename="settings.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


class Command(BaseCommand):
    """
    команда для создания БД заново
    """
    def handle(self, *args, **options):
        connect_params = read_config_db()
        database_name = 'mailing'

        conn = psycopg2.connect(dbname='postgres', **connect_params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")

        conn.commit()
        conn.close()
