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