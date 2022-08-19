
import mysql.connector

class MySqlConnection(object):
    def __init__(self):
        self.spotify_db = mysql.connector.connect(
            user='root',
            password='hotdog4567',
            host='localhost',
            port='3306',
            database='svapp1'
        )

    def query(self, query, args):
        cursor = self.spotify_db.cursor()
        cursor.execute(query, args)
        self.spotify_db.commit()

    def get_all(self, query, args):
        cursor = self.spotify_db.cursor(dictionary=True)
        cursor.execute(query, args)
        return cursor.fetchall()

