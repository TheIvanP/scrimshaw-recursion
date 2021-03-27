# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays 
                            (songplay_id SERIAL PRIMARY KEY, time_stamp timestamp, user_id int, level varchar, song_id varchar, artist_id varchar, session_id int, location varchar, user_agent varchar)""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users 
                        (user_id int PRIMARY KEY, first_name varchar, last_name varchar, gender varchar, level varchar);""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs 
                        (song_id varchar PRIMARY KEY, title varchar, duration numeric, artist_id varchar);""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists 
                            (artist_id varchar PRIMARY KEY, name varchar, location varchar, latitude numeric, longitude numeric);""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time 
                            (time_stamp timestamp PRIMARY KEY, hour int, day int, weekofyear int, month int, year int, weekday int);""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays (time_stamp, user_id, level, song_id, artist_id, 
                            session_id, location, user_agent)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level) 
                    VALUES (%s, %s, %s, %s, %s)""")

song_table_insert = ("""INSERT INTO songs (song_id, title, duration, artist_id) VALUES (%s, %s, %s, %s)""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude) VALUES (%s, %s, %s, %s, %s)""")

time_table_insert = ("""INSERT INTO time (time_stamp, hour, day, weekofyear, month, year, weekday) VALUES (%s, %s, %s, %s, %s, %s, %s)""")

# FIND SONGS

#song_select = ("""SELECT s.song_id, s.artist_id FROM songs AS s JOIN artists AS a ON s.artist_id = a.artist_id WHERE s.title=(%s) AND a.artist_name=(%s) AND s.duration=(%s)""")

song_select = ("""
        SELECT songs.song_id,
               artists.artist_id
        FROM  songs
          INNER JOIN artists
            ON songs.artist_id = artists.artist_id
        WHERE songs.title = %s
              AND
              artists.name = %s
              AND
              songs.duration = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]