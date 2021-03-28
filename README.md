# Sparkify song play database

Database and ETL pipeline for optimizing queries around what songs have been played by users.

---

### Files:
- etl.py
    - Main ETL proces to convert json files to table
 - eda.ipynb
    - Exploratory data analysis on resulting table plotting top 10 users
- etl.ipynb
    - Not used in etl pipeline or database; documentation of ETL development process
    
- sql_queries.py
    - sql strings for creating and inserting data into postgres
-   create_tables.py
    - script for creating and deleting table
    - run before etl.py as described below.
- ./data/
    - source json data
- test.ipynb
    - test selecting data from tables

---  

### How to run:
1. Place all files in directory together with /data/ folder containing json files for songs and logs
2. Have POSTGRES server running on localhost with enabled credentials for "host=127.0.0.1 user=student password=student"
3. From a terminal, run <python3 create_tables.py> this will create relevant database tables and Sparkify database
4. The application will create 'Sparkify' database
5. Run <python3 etl.py>
6. This will extract json files from data directory, transform and enrich the data with time information. Non existing data will be dropped.
7. The resulting data is saved in database in the following schema:
    
    - **Fact Table** 
        - `songplays` 
            - records in log data associated with song plays i.e. records with page NextSong
            songplay_id, time_stamp, user_id, level, song_id, artist_id, session_id, location, user_agent
    
    - **Dimension Tables**
        - `users` 
            - `user_id`
            - `first_name`
            - `last_name`
            - `gender`
            - `level`
        - `songs` 
            - `song_id`
            - `title`
            - `artist_id`
            - `year`
            - `duration`
        - `artists` 
            - `artist_id`
            - `name`
            - `location`
            - `latitude`
            - `longitude`
        - `songtime` 
            - `start_time`
            - `hour`
            - `day`
            - `week`
            - `month`
            - `year`
            - `weekday`