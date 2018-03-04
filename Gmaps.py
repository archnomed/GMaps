import urllib.request
import json
import sqlite3
import poly_manip
import webbrowser
from mako.template import Template

def plt_route(ls_coordinates):
    
    home = 'new google.maps.LatLng'+str(ls_coordinates[0][::-1])+';'
    pts = ""

    for i in ls_coordinates:
        pts += 'new google.maps.LatLng'+str(i[::-1])+','
    
    pts = pts[:-1]
    
    template = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Polyline Plot</title>

    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <style type="text/css">
    html { height: 100% }
    body { height: 100%; margin: 0; padding: 0 }
    #map_canvas { height: 100% }
    </style>
    <script type="text/javascript" src="http://maps.googleapis.com/maps/api/js"></script>

    <script>
        function initialize() {
            var homeLatlng = ${home}
            var myOptions = {
                zoom: 15,
                center: homeLatlng,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

            // create an array of coordinates
            var arrCoords = [
                ${pts}
            ];

            // draw the route on the map            
            var route = new google.maps.Polyline({
                path: arrCoords,
                strokeColor: "#00FF00",
                strokeOpacity: 1.0,
                strokeWeight: 4,
                geodesic: false,
                map: map
            }); 
        }

        google.maps.event.addDomListener(window, 'load', initialize);
    </script>
    </head>
    <body>
    <div id="map_canvas"></div>
    </body>
    </html>
    """
    return Template(template).render(home=home,pts=pts)


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

print('\n')
ls_coordinates = poly_manip.decode(polyline) 
result_html = plt_route(ls_coordinates)

fp = open('map.html','w')
fp.write(result_html)
fp.close()
webbrowser.open_new_tab('map.html')



