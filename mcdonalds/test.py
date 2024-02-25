import json
from sklearn.cluster import KMeans
import numpy as np
import folium
import pandas as pd


def trim_istanbul_and_shopping_centers():
    # Read the data
    with open('0_original_mcdonals.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    data = data['data']

    # Filter the data
    filtered_data = [store for store in data if 'İstanbul' in store['STORE_ADDRESS']]
    filtered_data = [store for store in filtered_data if store['IN_SHOPPING_CENTER'] != 1]
    # Discard unnecessary columns
    keys_to_keep = ['STORE_NAME', 'IN_SHOPPING_CENTER', 'STORE_OPEN_AT', 'STORE_CLOSE_AT', 'LATITUDE', 'LONGITUDE', 'STORE_ADDRESS']
    filtered_data = [{key: store[key] for key in keys_to_keep} for store in filtered_data]
    # Extract only the 'Hours' field from 'STORE_OPEN_AT' and 'STORE_CLOSE_AT'
    for store in filtered_data:
        store['STORE_OPEN_AT'] = store['STORE_OPEN_AT']['Hours']
        store['STORE_CLOSE_AT'] = store['STORE_CLOSE_AT']['Hours']
        store['STORE_TYPE'] = "McDonalds"

    # Write the data back to the file
    with open('1_istanbul_and_not_in_store.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False)

def group_stores():
    # Read the data
    with open('1_istanbul_and_not_in_store.json', 'r', encoding='utf-8') as f:
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
    with open('2_grouped.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

def visualize_clusters():
    # Read the data
    with open('2_grouped.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create a map centered around Istanbul
    m = folium.Map(location=[41.0082, 28.9784], zoom_start=10)

    # Define a color scheme for the clusters
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'black', 'gray', 'darkgreen']

    # Add the stores to the map
    for store in data:
        # Get the cluster color
        color = colors[store['CLUSTER']]

        # Add a marker for the store
        folium.Marker(
            location=[float(store['LATITUDE']), float(store['LONGITUDE'])],
            popup=f"Address: {store['STORE_ADDRESS']}, Cluster: {store['CLUSTER']}",
            icon=folium.Icon(color=color),
        ).add_to(m)

    # Save the map to an HTML file
    m.save('map.html')

def generate_route_plan():
    # Read the data
    with open('2_grouped.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Sort the stores in each cluster by latitude and longitude
    data.sort(key=lambda store: (store['CLUSTER'], float(store['LATITUDE']), float(store['LONGITUDE'])))

    # Prepare the data for the CSV file
    csv_data = []
    for store in data:
        csv_data.append([
            store['CLUSTER'],
            store['STORE_NAME'],
            store['STORE_ADDRESS'],
            store['STORE_OPEN_AT']['Hours'],
            store['STORE_CLOSE_AT']['Hours'],
        ])

    # Write the data to a CSV file
    df = pd.DataFrame(csv_data, columns=['Bölge', 'İsim', 'Adres', 'Açılış', 'Kapanış'])
    df.to_csv('route_plan.csv', index=False)

trim_istanbul_and_shopping_centers()
# group_stores()
# visualize_clusters()
# generate_route_plan()