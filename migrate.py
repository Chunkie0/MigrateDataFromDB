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

cursor.execute(f"CREATE TABLE deleted_archive(table_name NVARCHAR(20), value_id INTEGER, deletedAt DATETIME, deletedBy NVARCHAR(20));")

for table in chinook_tables:
    ch_table = table[0]
    if 'sqlite' not in ch_table:
        table_content = conn.execute(f"SELECT * FROM {ch_table}")
        columns = tuple([i[0] for i in table_content.description])
        values = table_content.fetchall()
        # auditions to check who and when created, updated and deleted(deleted_archive)
        cursor.execute(f"ALTER TABLE {ch_table} ADD COLUMN createdAt timestamp NOT NULL DEFAULT current_timestamp")
        cursor.execute(f"ALTER TABLE {ch_table} ADD COLUMN createdBy NVARCHAR(20) NULL")
        cursor.execute(f"ALTER TABLE {ch_table} ADD COLUMN updatedAt DATETIME DEFAULT NULL ON UPDATE current_timestamp")
        cursor.execute(f"ALTER TABLE {ch_table} ADD COLUMN updatedBy NVARCHAR(20) NULL")
        cursor.execute(f"CREATE TRIGGER trigger_{ch_table}_created BEFORE INSERT ON {ch_table} FOR EACH ROW SET NEW.createdBy = USER()")
        cursor.execute(f"CREATE TRIGGER trigger_{ch_table}_updated BEFORE UPDATE ON {ch_table} FOR EACH ROW SET NEW.updatedBy = USER()")
        cursor.execute(f"CREATE TRIGGER trigger_{ch_table}_deleted BEFORE DELETE ON {ch_table} FOR EACH ROW INSERT INTO deleted_archive(table_name, value_id, deletedAt, deletedBy) VALUES ('{ch_table}', OLD.{columns[0]}, current_timestamp, USER()) ")
        # migrates data from chinook database into music_shop database
        insert = "".join((f"INSERT INTO {ch_table} {columns} VALUES {str(values).replace('[', '').replace(']', '').replace('None', 'Null')}").split("'", len(columns)*2))
        cursor.execute(insert)


music_shop_db.commit()
music_shop_db.close()
