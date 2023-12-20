import psycopg

conn = psycopg.connect(user="postgres", host="localhost", password="postgres", autocommit=True)
cursor = conn.cursor()
cursor.execute("createdb chitter;")
cursor.execute("createdb chitter_test;")