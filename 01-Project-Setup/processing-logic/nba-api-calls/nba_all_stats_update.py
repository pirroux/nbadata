import requests
import csv
from datetime import datetime, timedelta
import time

# API URL for stats
url_stats = "https://www.balldontlie.io/api/v1/stats"

# Calculate the date for the previous day
yesterday = datetime.now() - timedelta(days=17)
formatted_yesterday = yesterday.strftime('%Y-%m-%d')

# Specify the parameters for the API request
params_stats = {
    'page': 0,
    'per_page': 100,
    'start_date': formatted_yesterday,
    'end_date': formatted_yesterday,
    # Add other query parameters as needed
}

# Specify the absolute path for existing CSV file
csv_filename_stats = '/Users/pierrecanadas/code/pirroux/personal_projects/nbadata/01-Project-Setup/data/all_stats.csv'

# Retry logic for stats
def make_request_with_retry_stats():
    max_retries = 30
    retry_delay = 2

    for attempt in range(max_retries):
        response = requests.get(url_stats, params=params_stats)

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

# Write stats data to existing CSV file
def write_stats_data(stats_data):
    with open(csv_filename_stats, 'a', newline='') as csvfile:  # Change 'w' to 'a'
        fieldnames = stats_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write stats data rows
        for stat in stats_data:
            writer.writerow(stat)

# Make the GET request with retry logic for stats
response_stats = make_request_with_retry_stats()

if response_stats:
    # Parse the JSON response for stats
    data_stats = response_stats.json()

    # Check if the 'meta' key is present in the stats response
    if 'meta' in data_stats:
        total_pages_stats = data_stats['meta'].get('total_pages')

        # Write stats data to existing CSV file
        write_stats_data(data_stats['data'])

        print(f"Stats data successfully retrieved and appended to {csv_filename_stats}.")
    else:
        print("No 'meta' key in the API response for stats.")
else:
    print("Request failed even after retries for stats.")
