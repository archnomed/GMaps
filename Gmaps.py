import urllib.request
import json
import sqlite3

endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
api_key = 'AIzaSyAyO4O0nLamNnnSVcpUbK6t87otvfWVYz0'

origin = input('Source :').replace(' ','+')
destination = input('Destination :').replace(' ','+')

print('\nO/P Format - ("Source", "Destination", "Polyline") \nPolyline encoding is a lossy compression algorithm that allows you to store a series of coordinates as a single string.\n')

nav_req = 'origin={}&destination={}&key={}'.format(origin,destination,api_key)

request = endpoint + nav_req
response = urllib.request.urlopen(request).read()

directions = json.loads(response.decode('utf-8'))
routes = directions['routes']
polyline = routes[0]['overview_polyline']['points']

conn = sqlite3.connect('dirinfo.db')
cur = conn.cursor()
query = "INSERT INTO dirinfo VALUES ('{}','{}','{}')".format(origin,destination,polyline)
cur.execute(query)
conn.commit()
cur.execute("SELECT * FROM dirinfo")

for i in cur.fetchall():
    print(i)
    print('\n')

conn.close()



