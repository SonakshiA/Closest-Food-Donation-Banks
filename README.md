# Objective
The United Nations Environment Programme estimates that India wastes 74 million tonnes of food each year. The goal is to develop a user-friendly web application that helps individuals locate the nearest food donation banks based on their current location. This application will aid in facilitating and encouraging community participation in food donation efforts, ultimately reducing food waste and supporting those in need.

# Overview
This application allows users to find the closest food donation banks in Mumbai based on their PIN code. By utilizing a .CSV file containing a list of food banks centered in Mumbai, the app identifies the five nearest food donation banks and visualizes the shortest route from the user's location to each food bank using Folium, OSMnx, and NetworkX.

# Working
1. The user enters their name and PIN Code in the application.
2. The application provides two options for users:
   
    A. **Map View:** Users can visualize the five closest food banks on an OpenStreetMap (OSM) map.
   
    B. **List View:** Users can access a detailed list of food banks that includes each bank's name, distance from the user, phone number, and address.

Additionally, users can view the shortest route from their input PIN code to the selected food bank using the List View. We use Dijkstra's algorithm to find the shortest path between the user's location and the food bank of their choice.

# Demo
[Watch Here!](https://drive.google.com/file/d/10tb9TH09Bqc6VIQC0pUL8xqvMZt8ifTa/view?usp=sharing)

# Using the Project
1. Ensure you have python, flask, osmnx, networkx, and geopy installed.
2. Use `python form.py` to run the flask application on your local server.

Feel free to fork this repo and add more features/contribute towards curating the dataset for Food Banks for different cities :D
