import requests
import pandas as pd
from sqlalchemy import create_engine

url = "https://api-formula-1.p.rapidapi.com/rankings/startinggrid"

querystring = {"race":"50"}

headers = {
	"x-rapidapi-key": "d3b26e1204msh9ad243881dc1646p1c1087jsnda8fc5f6236b",
	"x-rapidapi-host": "api-formula-1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())