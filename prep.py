''' Ignore this file '''
import sqlite3

conn = sqlite3.connect('dirinfo.db')
cur = conn.cursor()

cur.execute(''' CREATE TABLE dirinfo (
                Source text,
                Destination text,
                Polyline text
)''')

conn.commit()

conn.close()
