import requests
import csv
import time
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from the .env file
api_key = os.getenv('API_KEY')

# Check if the API key is loaded correctly
if not api_key:
    print("API Key not found! Make sure it's in the .env file.")
    exit()

# API URL
url = "https://api.balldontlie.io/v1/games"

# Specify the start date (YYYY-MM-DD)
start_date = '2017-09-01'  # Update this to your desired start date

# Calculate the current date as the end date
end_date = datetime.now().strftime('%Y-%m-%d')

# Initial parameters
params = {
    'page': 1,  # Start with page 1
    'per_page': 100,
    'start_date': start_date,
    'end_date': end_date,
}

# Headers with the API key (No Bearer prefix)
headers = {
    'Authorization': api_key
}

# Specify the absolute path for CSV file
csv_filename = '/Users/pierrecanadas/code/pirroux/personal_projects/nbadata/01-Project-Setup/data/games_data.csv'

# Write header to CSV file
def write_header():
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['id', 'date', 'home_team_id', 'home_team_name', 'home_team_score',
                      'visitor_team_id', 'visitor_team_name', 'visitor_team_score',
                      'season', 'period', 'status', 'time', 'postseason']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

# Write data to CSV file
def write_data(games_data):
    if games_data:  # Check if the list is not empty
        with open(csv_filename, 'a', newline='') as csvfile:
            fieldnames = ['id', 'date', 'home_team_id', 'home_team_name', 'home_team_score',
                          'visitor_team_id', 'visitor_team_name', 'visitor_team_score',
                          'season', 'period', 'status', 'time', 'postseason']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write data rows
            for game in games_data:
                row = {
                    'id': game.get('id'),
                    'date': game.get('date'),
                    'home_team_id': game.get('home_team', {}).get('id'),
                    'home_team_name': game.get('home_team', {}).get('full_name'),
                    'home_team_score': game.get('home_team_score'),
                    'visitor_team_id': game.get('visitor_team', {}).get('id'),
                    'visitor_team_name': game.get('visitor_team', {}).get('full_name'),
                    'visitor_team_score': game.get('visitor_team_score'),
                    'season': game.get('season'),
                    'period': game.get('period'),
                    'status': game.get('status'),
                    'time': game.get('time'),
                    'postseason': game.get('postseason')
                }
                writer.writerow(row)
    else:
        print("No data to write.")

# Retry logic
def make_request_with_retry(cursor):
    max_retries = 5
    retry_delay = 2
    params['page'] = cursor

    for attempt in range(max_retries):
        response = requests.get(url, params=params, headers=headers)
        print(f"Attempt {attempt + 1}: Status Code {response.status_code}")

        if response.status_code == 200:
            return response
        elif response.status_code == 429:
            print(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            break

    return None

# Loop over all pages
cursor = 1

# Write header to CSV file initially
write_header()

while True:
    response = make_request_with_retry(cursor)

    if response:
        data = response.json()

        # Debugging: Print out the data received
        print(f"Data received from cursor {cursor}: {data}")

        if 'meta' in data:
            # Write data to CSV file
            write_data(data['data'])

            # Check if there are more pages
            next_cursor = data['meta'].get('next_cursor')
            if next_cursor and next_cursor != cursor:
                cursor = next_cursor
                print(f"Data successfully retrieved from cursor {cursor}.")
            else:
                print("All pages retrieved. No more data available or next_cursor is the same as current.")
                break
        else:
            print("No 'meta' key in the API response.")
            break
    else:
        print("Request failed even after retries.")
        break

print(f"Data successfully written to {csv_filename}")
