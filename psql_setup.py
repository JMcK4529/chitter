import psycopg

conn = psycopg.connect(user="postgres", host="localhost", password="postgres", autocommit=True)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE chitter;")
cursor.execute("CREATE DATABASE chitter_test;")