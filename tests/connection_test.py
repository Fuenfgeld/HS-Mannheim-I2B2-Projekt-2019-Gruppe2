from unittest import TestCase
import psycopg2 as psy
from datenhaltung import connection as con

class TestConnection_zu_datenbank_aufbauen(TestCase):
    def test_connection_zu_datenbank_aufbauen(self):
        connection = psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.75", port="5432")
        return connection
        self.assertEqual(con.create_connection(), connection)