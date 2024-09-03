import requests
import pandas as pd
import os
import time
import csv

####get all teams

url = "https://www.balldontlie.io/api/v1/teams"

response = requests.get(url).json()

folder_path = '/Users/pierrecanadas/code/pirroux/personal_projects/nbadata/01-Project-Setup/data'
df = pd.DataFrame(response['data'])

csv_file_path = os.path.join(folder_path, 'data_all_teams.csv')
df.to_csv(csv_file_path,
          index=False)
print("Data saved successfully.")
