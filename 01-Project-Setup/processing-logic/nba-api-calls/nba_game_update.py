import requests
from dotenv import load_dotenv
import os
import csv
from datetime import datetime, timedelta
import time

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

# Calculate the date for the previous day
yesterday = datetime.now() - timedelta(days=1)
formatted_yesterday = yesterday.strftime('%Y-%m-%d')

# Specify the parameters for the API request
params = {
    'per_page': 100,
    'start_date': '2023-10-20',
    'end_date': formatted_yesterday,
}

# Headers with the API key (No Bearer prefix)
headers = {
    'Authorization': api_key
}

# Retry logic
def make_request_with_retry(page):
    max_retries = 5
    retry_delay = 2
    params['page'] = page

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

# Write data to existing CSV file
def write_data(games_data):
    csv_filename = '/Users/pierrecanadas/code/pirroux/personal_projects/nbadata/01-Project-Setup/data/games_data.csv'

    if len(games_data) > 0:
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = games_data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for game in games_data:
                writer.writerow(game)
    else:
        print("No games data to write.")

# Collect all pages of data
all_games_data = []
page = 1

while True:
    response = make_request_with_retry(page)

    if response:
        data = response.json()

        if 'meta' in data:
            all_games_data.extend(data['data'])
            total_pages = data['meta'].get('total_pages', 1)

            if page >= total_pages:
                print("All pages retrieved. No more data available.")
                break

            page += 1
            print(f"Page {page} retrieved. Moving to next page.")
        else:
            print("No 'meta' key in the API response.")
            break
    else:
        print("Request failed even after retries.")
        break

write_data(all_games_data)

print(f"Data successfully retrieved and written to your CSV.")
