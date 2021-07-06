import mysql.connector
import sqlite3

conn = sqlite3.connect('chinook.db')
cur = conn.cursor()

music_shop_db = mysql.connector.connect(
    host = "localhost",
    user = "admin",
    password = "password",
    database = "music_shop"
)

cursor = music_shop_db.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
chinook_tables = cur.fetchall()

cursor.execute("SET FOREIGN_KEY_CHECKS=0")

for table in chinook_tables:
    ch_table = table[0]
    if 'sqlite' not in ch_table:
        table_content = conn.execute(f"SELECT * FROM {ch_table}")
        columns = tuple([i[0] for i in table_content.description])
        values = table_content.fetchall()
        insert = "".join((f"INSERT INTO {ch_table} {columns} VALUES {str(values).replace('[', '').replace(']', '').replace('None', 'Null')}").split("'", len(columns)*2))
        cursor.execute(insert)
        
music_shop_db.commit()
music_shop_db.close()

# 100 times slower
''''
import mysql.connector
import sqlite3

conn = sqlite3.connect('chinook.db')
cur = conn.cursor()

music_shop_db = mysql.connector.connect(
    host = "localhost",
    user = "admin",
    password = "password",
    database = "music_shop"
)

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
chinook_tables = cur.fetchall()

cursor = music_shop_db.cursor()

for table in chinook_tables:
    ch_table = table[0]
    if 'sqlite' not in ch_table:
        cur.execute(f"SELECT * FROM {ch_table}")
        ch_table_content = cur.fetchall()
        for content in ch_table_content:
            content_list = list(content)
            while None in content_list:
                i = content_list.index(None)
                content_list[i] = 0
            content_tuple = tuple(content_list)
            cursor.execute("SET FOREIGN_KEY_CHECKS=0")
            cursor.execute(f"INSERT INTO {ch_table} VALUES {content_tuple}")
music_shop_db.commit()
music_shop_db.close()
''''''''''''''''''''''''''''''''''''
