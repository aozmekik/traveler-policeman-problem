import json
from sklearn.cluster import KMeans
import numpy as np
import folium
import pandas as pd


def group_stores():
    # Read the data
    with open('merge.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Prepare data for clustering
    coords = np.array([[float(store['LATITUDE']), float(store['LONGITUDE'])] for store in data])

    # Calculate the number of clusters based on the requirement of minimum 8 stores per cluster
    n_clusters = 7

    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(coords)

    # Assign each store to a cluster
    for i, store in enumerate(data):
        store['CLUSTER'] = int(kmeans.labels_[i])

    # Write the data back to the file
    with open('merged_grouped.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def delete_duplicate_addresses():
    # Load the data from the file
    df = pd.read_json('merged_grouped.json')

    # Remove duplicate rows based on STORE_ADDRESS
    df.drop_duplicates(subset='STORE_ADDRESS', inplace=True)

    # Write the data back to the file with utf-8 encoding
    df.to_json('merged_grouped.json', orient='records', force_ascii=False)


def visualize_clusters():
    # Read the data
    with open('merged_grouped.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create a map centered around Istanbul
    m = folium.Map(location=[41.0082, 28.9784], zoom_start=10)

    # Define a color scheme for the clusters
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'black', 'gray', 'darkgreen']

    # Define a dictionary for store icons
    icons = {'McDonalds': 'cloud', 'Starbucks': 'info-sign'}

    # Add the stores to the map
    for store in data:
        # Get the cluster color
        color = colors[store['CLUSTER']]

        # Get the store icon
        icon = icons[store['STORE_TYPE']]

        # Add a marker for the store
        folium.Marker(
            location=[float(store['LATITUDE']), float(store['LONGITUDE'])],
            popup=folium.Popup(f'Address: {store["STORE_ADDRESS"]}, <a href="{create_google_maps_url((float(store["LATITUDE"]), float(store["LONGITUDE"])))}" target="_blank">Link</a>, Cluster: {store["CLUSTER"] + 1}, Store Type: {store["STORE_TYPE"]}'),
            icon=folium.Icon(color=color, icon=icon),
        ).add_to(m)

    # Save the map to an HTML file
    m.save('map.html')

from concorde.tsp import TSPSolver
from numpy import array


def create_google_maps_url(coord):
    url = "https://www.google.com/maps/dir/"
    url += f"{coord[0]},{coord[1]}/"
    return url

def generate_route_plan():
    # Read the data
    with open('merged_grouped.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Prepare the data for the CSV file
    csv_data = []

    # Get the unique clusters
    clusters = set(store['CLUSTER'] for store in data)

    # For each cluster, find the optimal route
    for cluster in clusters:
        # Get the stores in this cluster
        stores = [store for store in data if store['CLUSTER'] == cluster]

        # Append the route data to the CSV data
        for i, store in enumerate(stores):
            csv_data.append([
                store['CLUSTER'] + 1,
                store['STORE_TYPE'],
                store['STORE_NAME'],
                store['STORE_ADDRESS'],
                str(store['LATITUDE']) + ', ' + str(store['LONGITUDE']),
                store['STORE_OPEN_AT'],
                store['STORE_CLOSE_AT'],
                create_google_maps_url((float(store['LATITUDE']),float(store['LONGITUDE'])))
            ])

    # Write the data to a CSV file
    df = pd.DataFrame(csv_data, columns=['Cluster', 'Store Type', 'Store Name', 'Store Address', 'Coordinates', 'Store Open At', 'Store Close At', 'Google Link'])
    df.to_csv('route_plan.csv')


# group_stores()
# delete_duplicate_addresses()
visualize_clusters()
generate_route_plan()