
import mysql.connector

spotify_db = mysql.connector.connect(
            user='root',
            password='hotdog4567',
            host='localhost',
            port='3306',
            database='spotifyapp'
        )

cursor = spotify_db.cursor()
#cursor.execute('CREATE TABLE tracks(name varchar(100) primary key, img_url varchar(100), artist_name varchar(100), album_name varchar(100))')
cursor.execute('CREATE TABLE IF NOT EXISTS loginfo(username varchar(100), password varchar(100), id int auto_increment primary key, email_id varchar(100), verification int)')
spotify_db.commit()
cursor.close()
spotify_db.close()