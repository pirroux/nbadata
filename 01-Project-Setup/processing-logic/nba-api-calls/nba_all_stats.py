import requests
import csv
from datetime import datetime, timedelta
import time

# API URL for stats
url_stats = "https://www.balldontlie.io/api/v1/stats"

# Specify the start date (YYYY-MM-DD)
start_date_stats = '2017-09-01'  # Update this to your desired start date

# Calculate the current date as the end date
end_date_stats = datetime.now().strftime('%Y-%m-%d')

# Initial parameters for stats
params_stats = {
    'page': 0,
    'per_page': 100,
    'start_date': start_date_stats,
    'end_date': end_date_stats,
    # Add other query parameters as needed
}

# Specify the absolute path for CSV file for stats
csv_filename_stats = '/Users/pierrecanadas/code/pirroux/personal_projects/nbadata/01-Project-Setup/data/all_statsTEST.csv'

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

# Write stats data to CSV file
def write_stats_data(stats_data):
    with open(csv_filename_stats, 'a', newline='') as csvfile:
        fieldnames_stats = stats_data[0].keys()
        writer_stats = csv.DictWriter(csvfile, fieldnames=fieldnames_stats)

        # Write stats data rows
        for stat in stats_data:
            writer_stats.writerow(stat)

# Loop over all pages for stats
total_pages_stats = None
request_counter_stats = 0

while True:
    # Make the GET request with retry logic for stats
    response_stats = make_request_with_retry_stats()

    if response_stats:
        # Parse the JSON response for stats
        data_stats = response_stats.json()

        # Check if the 'meta' key is present in the stats response
        if 'meta' in data_stats:
            total_pages_stats = data_stats['meta'].get('total_pages')

            # If it's the first page, write header to CSV file
            if params_stats['page'] == 0:
                with open(csv_filename_stats, 'w', newline='') as csvfile:
                    fieldnames_stats = data_stats['data'][0].keys()
                    writer_stats = csv.DictWriter(csvfile, fieldnames=fieldnames_stats)
                    writer_stats.writeheader()

            # Write stats data to CSV file
            write_stats_data(data_stats['data'])

            # Increment the request counter
            request_counter_stats += 1

            # Check if there are more pages
            if 'next_page' in data_stats['meta'] and data_stats['meta']['next_page'] is not None:
                # Update the page parameter for the next request
                params_stats['page'] = data_stats['meta']['next_page']
            else:
                # Break the loop if there are no more pages
                break
        else:
            print("No 'meta' key in the API response for stats.")
            break
    else:
        # Break the loop if the request fails even after retries
        break

    print(f"Stats data successfully retrieved from page {params_stats['page']} of {total_pages_stats} pages.")

print(f"Stats data successfully written to {csv_filename_stats}")
