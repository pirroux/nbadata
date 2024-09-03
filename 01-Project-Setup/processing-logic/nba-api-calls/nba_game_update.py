import requests
import csv
from datetime import datetime, timedelta
import time

# API URL
url = "https://www.balldontlie.io/api/v1/games"

# Calculate the date for the previous day
yesterday = datetime.now() - timedelta(days=1)
formatted_yesterday = yesterday.strftime('%Y-%m-%d')

# Specify the parameters for the API request
params = {
    'page': 0,
    'per_page': 100,
    'start_date': formatted_yesterday,
    'end_date': formatted_yesterday,
    # Add other query parameters as needed
}

# Specify the absolute path for existing CSV file
csv_filename = '/Users/pierrecanadas/code/pirroux/personal_projects/nbadata/01-Project-Setup/data/games_data.csv'

# Retry logic
def make_request_with_retry():
    max_retries = 30
    retry_delay = 2

    for attempt in range(max_retries):
        response = requests.get(url, params=params)

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

# Write data to existing CSV file
def write_data(games_data):
    with open(csv_filename, 'a', newline='') as csvfile:  # Change 'w' to 'a'
        fieldnames = games_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write data rows
        for game in games_data:
            writer.writerow(game)

# Make the GET request with retry logic
response = make_request_with_retry()

if response:
    # Parse the JSON response
    data = response.json()

    # Check if the 'meta' key is present in the response
    if 'meta' in data:
        total_pages = data['meta'].get('total_pages')

        # Write data to existing CSV file
        write_data(data['data'])

        print(f"Data successfully retrieved and appended to {csv_filename}.")
    else:
        print("No 'meta' key in the API response.")
else:
    print("Request failed even after retries.")
