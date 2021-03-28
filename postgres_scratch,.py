#%%
import psycopg2
#conn = psycopg2.connect(dbname="test", user="postgres", password="example", host="0.0.0.0",port=5432)
conn = psycopg2.connect(dbname="template1", user="postgres", password="postgres", host="0.0.0.0",port=5432)
#%%
#%%
conn.set_session(autocommit=True)
cur = conn.cursor()
#%%
cur.execute("""SELECT *
FROM pg_stat_activity
WHERE datname = '<database_name>';""")

#%%
conn.close()
#%%‚
# create sparkify database with UTF8 encoding


cur.execute("DROP DATABASE sparkifydb")
#%%

cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")
#%%


cur.execute("""CREATE TABLE films (
    code        char(5),
    title       varchar(40),
    did         integer,
    date_prod   date,
    kind        varchar(10),
    len         interval hour to minute,
    CONSTRAINT code_title PRIMARY KEY(code,title)
);""")

cur.execute("""INSERT INTO films VALUES
    ('UA502', 'Bananas', 105, '1971-07-13', 'Comedy', '82 minutes');""")

cur.execute("SELECT * FROM films;")

cur.fetchone()
#%%