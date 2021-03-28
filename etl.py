import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """Write artist data to database. Extracts a list of artist_data values 
    from a json file formatted in lines
    
    Args: 
        cur: psycopg2 cursor object
        filepath: path to directory with json files
    
    """
    
    # open song file with lines = true to parse line by line
    df = pd.read_json(filepath, lines=True)

    # insert song record - select row from dataframe, cast it to list for insertion
    song_data = df[['song_id', 'title', 'artist_id','year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert song record - select row from dataframe, cast it to list for insertion
    artist_data = df[['artist_id','artist_name', 'artist_location','artist_latitude', 'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """creates songplay fact table associating songs data with log data based on artist name, song title and duration
    
    Args: 
        cur: psycopg2 cursor object
        filepath: path to directory with json files
    """
    
    
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    # drops non existing data for specific columns
    # .where returns nans in place of missing values, use boolean indexing to avoid this! 
    df = df[df['page'] == 'NextSong']
    

    # convert timestamp column to datetime; in ms to match format for 
    t = pd.to_datetime(df['ts'], unit='ms')

    # Handle pandas NaT type before inserting as NaT is not supported in timestamp postgres type 
    # (or possibly with current constraints on table)
    #t = t.replace([pd.NaT, [None]])
    
    # insert time data records. 
#    time_data = time_data = [t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.dayofweek]
    time_data = time_data = [t, t.dt.hour, t.dt.day, t.dt.isocalendar().week, t.dt.month, t.dt.year, t.dt.dayofweek]
    column_labels = ['timestamp', 'hour', 'day', 'weekofyear', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(data=dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table 
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None
        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """Process all json files in directory tree using function passed in arg
    prints files found and number of files processed to stdout
    
    Args: 
        cur: psycopg2 cursor object
        conn: psycopg2 connection object
        filepath: path to directory with json files
        func: function to apply
    """

    
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()