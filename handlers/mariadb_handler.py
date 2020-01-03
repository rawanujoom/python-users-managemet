import mysql.connector as mariadb
from configuration.config import CONFIG


class MariaDbHandler():
    def __init__(self):
        self.mariadb_connection = mariadb.connect(user=CONFIG["MYSQL_USER"], password=CONFIG["MYSQL_PASS"],
                                                  database=CONFIG["MYSQL_DB"],
                                                  host=CONFIG["MYSQL_HOST"])
        self.cursor = self.mariadb_connection.cursor()

    def select(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor
        except Exception as e:
            return None

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.mariadb_connection.commit()
            return True
        except Exception as e:
            return False

    def close_connection(self):
        self.cursor.close()
