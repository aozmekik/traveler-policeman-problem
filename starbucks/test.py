import json

def trim_istanbul_and_starbucks():
    # Read the data
    with open('0_original_starbucks.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    filtered_data = data['stores']

    # Discard unnecessary columns and map the data
    keys_to_keep = ['name', 'coordinates', 'address']
    filtered_data = [{key: store[key] for key in keys_to_keep} for store in filtered_data]

    disclude =['avm', 'center', 'merkez', 'alisveris', 'universitesi', 'universite', 'üniversitesi', 'üniversite',
     'hastane', 'hastanesi', 'hospital', 'station', 'mall', 'plaza', 'zemin', 'canpark', 'opet', 'ofis', 'optimum', 'outlet', 'metropol', 'tower', 'towers']
    # Filter out stores with 'avm' in the name
    filtered_data = [store for store in filtered_data if all(keyword not in store['name'].lower() for keyword in disclude)]
    
    # Map the data to the desired format
    for store in filtered_data:
        store['STORE_NAME'] = store.pop('name')
        store['LATITUDE'] = str(store['coordinates'].pop('latitude'))
        store['LONGITUDE'] = str(store['coordinates'].pop('longitude'))
        store['STORE_ADDRESS'] = ' '.join([value for value in store['address'].values() if value])
        store['STORE_OPEN_AT'] = 7
        store['STORE_CLOSE_AT'] = 24

        del store['coordinates']
        del store['address']
        store['STORE_TYPE'] = "Starbucks"

    # Delete stores if 'avm', 'center', or 'merkez' is in the address
    filtered_data = [store for store in filtered_data if not any(keyword in store['STORE_ADDRESS'].lower() for keyword in disclude)]

    # Write the data back to the file
    with open('1_istanbul_and_not_in_store.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False)

trim_istanbul_and_starbucks()