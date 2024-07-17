from flask import Flask, request, render_template , url_for
import pandas as pd
import osmnx as ox
import requests
import folium
import webbrowser
import os
from sortedcontainers import SortedList
from geopy.distance import distance
import json
from pprint import pprint
import networkx as nx
import os

global home_location


def process_data(pin,action):
    data = pd.read_csv('Food_Donation_Banks.csv')
    #print(data.head(n=10))
    BASE_URL = os.getenv('BASE_URL')
    EMAIL = os.getenv('EMAIL')

    pincode = pin
    country = 'india'
    response = requests.get(f"{BASE_URL}&email={EMAIL}&postalcode={pincode}&country={country}")
    try:
        data2 = response.json()
    except json.JSONDecodeError:
        data2 = None
    if not data2:
        #print("Invalid PIN entered")
        return render_template("error.html")
    else:
        latitude = data2[0].get('lat')
        longitude = data2[0].get('lon')

        #plotting source
        global home_location
        home_location = float(latitude), float(longitude)
        m = folium.Map(location=home_location,width=1200,height=800)
        folium.Marker(home_location,popup="Source",icon=folium.Icon(color='red')).add_to(m)
        m.save("templates/myMap.html")
        #webbrowser.open("myMap.html")


        #data structure to store the NGOs based on shortest distance
        sorted_list = SortedList(key = lambda x: x[3]) #key function that sorts items based on the distance
        def add_item(sorted_list,name,lat,long,distance,phone_no,address):
            sorted_list.add((name,lat,long,distance,phone_no,address))


        #calculating distance from home location to each NGO 
        for index, row in data.iterrows():
            location = float(row['Latitude']), float(row['Longitude'])
            dist = distance(location,home_location)
            dist_km = round(dist.km,2)
            phone_no = str(int(row['Phone No'])) if pd.notna(row['Phone No']) else 'Not Mentioned'
            add_item(sorted_list,row['Name'],row['Latitude'],row['Longitude'],dist_km,phone_no,row['Address'])
        
        #print(sorted_list)
        df = pd.DataFrame(sorted_list,columns=['NGO','Latitude','Longitude','Distance (KM)','Phone No','Address'])
        columns_to_hide = ['Latitude', 'Longitude']

        
        #mapping all NGOs based on distance
        i=0
        for i, (name, lat, long, dist,phone,add) in enumerate(sorted_list):
            if i < 5:  # Show closest 5 locations
               location = float(lat), float(long)
               folium.Marker(location, popup=name + " " + str(dist) + " km").add_to(m)
               i+=1
        m.save("templates/NGOs.html")
        if action=='Find On Map':
         return render_template("NGOs.html")
        else:
           return render_template("info.html",organizations=sorted_list)
        

app = Flask(__name__,template_folder='templates') # initializes a new Flask web application instance.

@app.route('/')
def index():
   return render_template('form.html')

@app.route('/submit', methods =["POST"])
def submit():
   name = request.form["name"]
   pin = request.form["pin"]
   action = request.form['action']
   return process_data(pin,action)


    
@app.route('/shortest_path',methods=['POST'])
def shortest_path():
    # Define origin and destination coordinates
    origin_point = home_location
    destination_latitude = request.form['lat']
    destination_longitude = request.form['lon']
    name_of_org = request.form['name']
    dist = request.form['dist']
    destination_point = float(destination_latitude), float(destination_longitude)

    # Download the graph for Mumbai
    G = ox.graph_from_point(center_point=origin_point, dist=15000, network_type='drive')

    # Get nearest nodes to the origin and destination points
    origin_node = ox.distance.nearest_nodes(G, X=origin_point[1], Y=origin_point[0])
    destination_node = ox.distance.nearest_nodes(G, X=destination_point[1], Y=destination_point[0])

    # Calculate the shortest path
    try:
        shortest_path = nx.shortest_path(G, origin_node, destination_node, weight='length')

        # # Print the path
        # print("Shortest path nodes:")
        # for node in shortest_path:
        #     print(f"Node: {node}, Latitude: {G.nodes[node]['y']}, Longitude: {G.nodes[node]['x']}")

        # Get route coordinates
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_path]

        # Create a Folium map
        m = folium.Map(location=origin_point, zoom_start=14)

        # Add the route to the map
        folium.PolyLine(locations=route_coords, color='blue', weight=5, opacity=0.7).add_to(m)

        # Add markers for the origin and destination
        folium.Marker(location=origin_point, popup='Origin', icon=folium.Icon(color='red')).add_to(m)
        folium.Marker(location=destination_point, popup=name_of_org + " " + dist + " km", icon=folium.Icon(color='blue')).add_to(m)

        # Save the map to an HTML file
        m.save("templates/shortest_path_map.html")
        #webbrowser.open("shortest_path_map.html")
        print("Map saved to 'shortest_path_map.html'.")

    except nx.NetworkXNoPath:
        print("No path found between the specified nodes.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return render_template("shortest_path_map.html")
 
if __name__=='__main__':
   app.run(debug=True)


