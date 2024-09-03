import requests
import csv
import time
from datetime import datetime

# API URL
url = "https://www.balldontlie.io/api/v1/games"

# Specify the start date (YYYY-MM-DD)
start_date = '2017-09-01'  # Update this to your desired start date

# Calculate the current date as the end date
end_date = datetime.now().strftime('%Y-%m-%d')

# Initial parameters
params = {
    'page': 0,
    'per_page': 100,
    'start_date': start_date,
    'end_date': end_date,
    # Add other query parameters as needed
}

# Specify the absolute path for CSV file
csv_filename = '/Users/pierrecanadas/code/pirroux/personal_projects/nbadata/01-Project-Setup/data/games_data.csv'

# Write header to CSV file
def write_header():
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['id', 'date', 'home_team_id', 'visitor_team_id', 'season', 'period', 'status', 'time', 'postseason']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

# Write data to CSV file
def write_data(games_data):
    with open(csv_filename, 'a', newline='') as csvfile:
        fieldnames = games_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Write data rows
        for game in games_data:
            writer.writerow(game)

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

# Loop over all pages
total_pages = None
request_counter = 0

while True:
    # Make the GET request with retry logic
    response = make_request_with_retry()

    if response:
        # Parse the JSON response
        data = response.json()

        # Check if the 'meta' key is present in the response
        if 'meta' in data:
            total_pages = data['meta'].get('total_pages')

            # If it's the first page, write header to CSV file
            if params['page'] == 0:
                write_header()

            # Write data to CSV file
            write_data(data['data'])

            # Increment the request counter
            request_counter += 1

            # Check if there are more pages
            if 'next_page' in data['meta'] and data['meta']['next_page'] is not None:
                # Update the page parameter for the next request
                params['page'] = data['meta']['next_page']
            else:
                # Break the loop if there are no more pages
                break
        else:
            print("No 'meta' key in the API response.")
            break
    else:
        # Break the loop if the request fails even after retries
        break

    print(f"Data successfully retrieved from page {params['page']} of {total_pages} pages.")

print(f"Data successfully written to {csv_filename}")
