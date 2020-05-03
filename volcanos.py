import pandas
import folium

map = folium.Map(location=[39.11,-98.08], zoom_start=3, tiles = "Stamen Terrain") #this creates the base layer for the map
fg = folium.FeatureGroup(Name='My Map')#this is a way to keep your code organized because you can keep loading in features into a feature group.
#this is a base layer


######BEGINNING OF THE SECOND LAYER OF THE MAP -- THE VOLCANO MARKERS
fgv = folium.FeatureGroup(Name="Volcanos") #Creating a new feature group layer 
volcanos = pandas.read_csv("course/section17map/volcanos.csv") #reading data on the USA volcanos
lat = list(volcanos["LAT"])#just taking the data from the LAT column and putting it into a native python list for use in a for loop
lon = list(volcanos["LON"])
elev = list(volcanos["ELEV"])
nam = list(volcanos["NAME"])
voltype = list(volcanos["TYPE"])
status = list(volcanos["STATUS"])


####Style points here
html = """
Volcano name:<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
""" #need to reveiw html code 
#<br> is a break

def colorproducer(el): #this is function that returns a differnet value depending on the elevation data in that element. Will run inside the for loop.
    if el > 3000:
        return 'green'
    elif el > 2000:
        return 'red'
    else:
        return 'blue'

for la, lo, el, name in zip(lat, lon, elev, nam): #when iterating through two lists you have to use the zip function
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100) #this iframe is used to load in an iframe that sets the visual aspects of the marker
    fgv.add_child(folium.CircleMarker(location=[la,lo], popup=folium.Popup(iframe), fill_color=colorproducer(el), color='grey', fill_opacity='0.7'))#this is considered a "Child" of the map object. This is making a market on the map.



#######BEGINNING OF THE THIRD LAYER ON THE MAP - THE COUNTRY POLYGONS
fgp = folium.FeatureGroup(Name="Populations")
fgp.add_child(folium.GeoJson(data=open('course/section17map/world.json', 'r', encoding='utf-8-sig').read(), #This line of code is loading in the polygons #'r' is for read mode 
#need encoding...research why...it was suggested by the error message
#new folium requires string input not a file so we use a .read() at the end of the open statement to get this
style_function = lambda x: {'fillColor':'yellow' if x['properties']['POP2005'] <=50000000 else #using a lambda functon to stylize. lambda is a unnamed function which works great for small tasks in code.
'orange' if x['properties']['POP2005'] <100000000 
else 'purple' if  x['properties']['POP2005'] <2000000
else 'blue' if x['properties']['POP2005'] <1000000000
else 'black'}))     
#what it is going is running through every single part of the dictionary, where each country is its own dictionary that has data attached and saying in "properties" 
#if the population is less than XXXX than change the fillColor to ''


map.add_child(fgp)
map.add_child(fgv)
map.add_child(fg)
map.add_child(folium.LayerControl())#layer control has to be added after the feature group
map.save("course/section17map/ImTheMap.html") #creates a file or overwrites existing html file
