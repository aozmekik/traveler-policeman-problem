# Istanbul Traveler

This project focuses on merging, standardizing, and visualizing McDonald's and Starbucks (Murderers) locations in Istanbul on a web-based map application. The goal is to provide a unified view of these fast-food outlets across the city, making it easier for policemens to find their nearest location.

## Features

- **Data Standardization**: Converts raw location data from both McDonald's and Starbucks into a standardized format.
- **Data Merging**: Combines standardized data into a single dataset for easier processing and visualization.
- **Map Visualization**: Displays the locations on an interactive map, allowing policemens to visually identify nearby outlets.

## Implementation Details

### Data Standardization

The raw data from Starbucks and McDonald's are in different formats. The Starbucks data, found in `starbucks/0_original_starbucks.json`, contains detailed information about each store, including coordinates, address, and opening hours.


```1:34:starbucks/0_original_starbucks.json
{
    "stores": [
        {
            "recommendation": {
                "isUsual": false
            },
            "storeNumber": "31521-107344",
            "id": "6015",
            "name": "Sultanahmet Divan Yolu No:76",
            "phoneNumber": "02125272419",
            "coordinates": {
                "latitude": 41.00824,
                "longitude": 28.97379
            },
            "regulations": [],
            "address": {
                "streetAddressLine1": "Alemdar Mah. Divanyolu Cad. No:76/A",
                "streetAddressLine2": null,
                "streetAddressLine3": null,
                "city": "Istanbul",
                "countrySubdivisionCode": "34",
                "countryCode": "TR",
                "postalCode": "34110"
            },
            "timeZoneInfo": {
                "currentTimeOffset": 180,
                "windowsTimeZoneId": "Turkey Standard Time",
                "olsonTimeZoneId": "GMT+00:00 Europe/Istanbul"
            },
            "brandName": "Starbucks",
            "ownershipTypeCode": "LS",
            "curbside": {
                "state": "notSupported"
            },
```


The McDonald's data, embedded within the HTML file `mcdonalds/map.html`, includes markers and popups for each location.


```517:520:mcdonalds/map.html

        
            
                var html_946d0fc6ffcdcb23c9786dc43da3925d = $(`<div id="html_946d0fc6ffcdcb23c9786dc43da3925d" style="width: 100.0%; height: 100.0%;">Address: Süzer Bulvarı Şehr-i Bazar AVM G-Blok No:9 Bahçeşehir 3. Cadde/İstanbul, Cluster: 1</div>`)[0];
```


### Data Merging

After standardizing the data formats, the next step is to merge them into a single JSON file, `merge.json`, which contains a unified view of all locations.


```1:34:merge.json
[
    {
        "STORE_NAME": "Sultanahmet Divan Yolu No:76",
        "LATITUDE": "41.00824",
        "LONGITUDE": "28.97379",
        "STORE_ADDRESS": "Alemdar Mah. Divanyolu Cad. No:76/A Istanbul 34 TR 34110",
        "STORE_OPEN_AT": 7,
        "STORE_CLOSE_AT": 24,
        "STORE_TYPE": "Starbucks"
    },
    {
        "STORE_NAME": "Cemberlitas",
        "LATITUDE": "41.00869",
        "LONGITUDE": "28.96963",
        "STORE_ADDRESS": "Yeniceriler Caddesi Mimar Hayrettin Mahallesi Istanbul 34 TR 34126",
        "STORE_OPEN_AT": 7,
        "STORE_CLOSE_AT": 24,
        "STORE_TYPE": "Starbucks"
    },
    {
        "STORE_NAME": "Istanbul Galataport HOSS",
        "LATITUDE": "41.02447",
        "LONGITUDE": "28.98042",
        "STORE_ADDRESS": "Kilicali Pasa Mahallesi Kemankes Sokak No 40 A Galataport Beyoglu Istanbul Istanbul 34 TR 34425",
        "STORE_OPEN_AT": 7,
        "STORE_CLOSE_AT": 24,
        "STORE_TYPE": "Starbucks"
    },
    {
        "STORE_NAME": "Tophane Reserve",
        "LATITUDE": "41.02586",
        "LONGITUDE": "28.98042",
        "STORE_ADDRESS": "Mumhane Cad. Beyoglu Istanbul 33 TR 34425",
        "STORE_OPEN_AT": 7,
```


### Map Application

The map application is web-based, utilizing Leaflet.js for rendering the map and the locations of Starbucks and McDonald's in Istanbul. The application reads from the merged and standardized JSON file to plot each location on the map.

The map initialization and marker plotting are done through JavaScript embedded within an HTML file. Here's a snippet showing how a marker is added:


```520:525:mcdonalds/map.html
                var html_946d0fc6ffcdcb23c9786dc43da3925d = $(`<div id="html_946d0fc6ffcdcb23c9786dc43da3925d" style="width: 100.0%; height: 100.0%;">Address: Süzer Bulvarı Şehr-i Bazar AVM G-Blok No:9 Bahçeşehir 3. Cadde/İstanbul, Cluster: 1</div>`)[0];
                popup_287b27b92e6e6079ae7ce179de320f02.setContent(html_946d0fc6ffcdcb23c9786dc43da3925d);
            
        

        marker_251ea58029bc398fbf0b78fa899fd07b.bindPopup(popup_287b27b92e6e6079ae7ce179de320f02)
```


## Running the Application

To run the map application:

1. Ensure you have a web server set up to serve the HTML and JSON files.
2. Open the HTML file in a browser. The map should load with markers indicating the locations of Starbucks and McDonald's outlets.

## Conclusion

This project simplifies the process of finding Starbucks and McDonald's locations in Istanbul by merging and standardizing data from both brands and visualizing them on an interactive map.