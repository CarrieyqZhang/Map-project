import folium
import pandas

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map = folium.Map(location = [37.33536652033734, -121.88102858673733], zoom_start=6, tiles = "Stamen Terrain")
data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

def color_producer(elevation):
    if elevation < 1500:
        return 'green'
    elif 1500 <= elevation < 2000:
        return 'blue'
    elif 2000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

fgv = folium.FeatureGroup(name = "Valcanoes")

for la, ln, el, name in zip(lat,lon, elev,name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.Marker(location=[la, ln], popup=folium.Popup(iframe), icon = folium.Icon(color = color_producer(el))))

fgp = folium.FeatureGroup(name = "Population")
fgp.add_child(folium.GeoJson(data = open("world.json",'r',encoding='utf-8-sig').read(), style_function=lambda x: {'fillColor':'green' if 10**7<x["properties"]["POP2005"]
else 'orange' if 10**7<=x["properties"]["POP2005"]<10**8  else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map1.html")