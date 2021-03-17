#%%
import psycopg2
#conn = psycopg2.connect(dbname="test", user="postgres", password="example", host="0.0.0.0",port=5432)
conn = psycopg2.connect(dbname="database", user="username", password="secret", host="0.0.0.0",port=5432)
#%%
cur = conn.cursor()

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