import requests
import pandas as pd
import os
import time
import csv


###get all players
all_players_data = []
num_pages = 50

for page in range(1, num_pages +1):
    url = "https://www.balldontlie.io/api/v1/players"
    params= {
        "page" : 1,
        "per_page" : 100,
    }
    response = requests.get(url, params=params).json()
    # Append data to the list
    all_players_data.extend(response['data'])

folder_path = '/Users/pierrecanadas/code/pirroux/personal_projects/nbadata/01-Project-Setup/data'
df = pd.DataFrame(all_players_data)

csv_file_path = os.path.join(folder_path, 'data_all_players.csv')
df.to_csv(csv_file_path,
          index=False)
print("Data saved successfully.")
