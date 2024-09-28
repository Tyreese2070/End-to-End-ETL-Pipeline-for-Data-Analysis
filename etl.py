import requests
import csv
import sqlite3

# https://apilist.fun/api/ergast-f1

# Request data from Ergast F1 API
def extract_data(season):
    url = f'http://ergast.com/api/f1/{season}.json'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from API: {response.status_code}")
    
# Transform API data
def transform_data(raw_data):
    races = raw_data['MRData']['RaceTable']['Races']
    transformed_data = []
    for race in races:
        race_info = {
            'race_name': race['raceName'],
            'circuit_name': race['Circuit']['circuitName'],
            'date': race['date'],
            'location': race['Circuit']['Location']['locality'],
            'country': race['Circuit']['Location']['country']
        }
        # Append the race_info to the transformed_data list here
        transformed_data.append(race_info)
    return transformed_data

# Load data to csv file
def load_to_csv(transformed_data, file_name='f1_season_data'):
    fieldnames = ['race_name', 'circuit_name', 'date', 'location', 'country']
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for data in transformed_data:
            writer.writerow(data)
            
# Load data to database with sqlite
def load_to_database(transformed_data, db_name='f1_data.db'):
    # Connect to sqlite3 database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS race_data (
            race_name TEXT,
            circuit_name TEXT,
            date TEXT,
            location TEXT,
            country TEXT
        )
    ''')

    for data in transformed_data:
        for data in transformed_data:
            cursor.execute('''
            INSERT INTO race_data (race_name, circuit_name, date, location, country) 
            VALUES (?, ?, ?, ?, ?)
        ''', (data['race_name'], data['circuit_name'], data['date'], data['location'], data['country']))
    
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

def pipeline(season):
    raw_data = extract_data(season)
    transformed_data = transform_data(raw_data)
    
    load_to_csv(transformed_data, file_name = f'f1_season_data_{season}.csv')
    load_to_database(transformed_data, db_name=f'f1_data_{season}.db')
    
pipeline(2024)