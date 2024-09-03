import csv
import requests
import time

# API URL for season averages
url_season_averages = "https://www.balldontlie.io/api/v1/season_averages"

# Specify the absolute path for the CSV file
csv_filename_season_averages = '/path/to/your/csv/file/all_season_averages.csv'

# Specify the desired season
desired_season = 2018  # Replace with the desired season

# Initial parameters for season averages
params_season_averages = {
    'season': desired_season,
    'per_page': 100,  # Adjust as needed
}

# Retry logic for season averages
def make_request_with_retry_season_averages():
    max_retries = 30
    retry_delay = 2

    for attempt in range(max_retries):
        response = requests.get(url_season_averages, params=params_season_averages)

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

# Write season averages data to CSV file
def write_season_averages_data(season_averages_data):
    with open(csv_filename_season_averages, 'a', newline='') as csvfile:
        fieldnames_season_averages = season_averages_data[0].keys()
        writer_season_averages = csv.DictWriter(csvfile, fieldnames=fieldnames_season_averages)

        # Write season averages data rows
        for average in season_averages_data:
            writer_season_averages.writerow(average)

# Loop over all pages for season averages
total_pages_season_averages = None
request_counter_season_averages = 0

while True:
    # Make the GET request with retry logic for season averages
    response_season_averages = make_request_with_retry_season_averages()

    if response_season_averages:
        # Parse the JSON response for season averages
        data_season_averages = response_season_averages.json()

        # Check if the 'meta' key is present in the season averages response
        if 'meta' in data_season_averages:
            total_pages_season_averages = data_season_averages['meta'].get('total_pages')

            # If it's the first page, write header to CSV file
            if params_season_averages.get('page', 0) == 0:
                with open(csv_filename_season_averages, 'w', newline='') as csvfile:
                    fieldnames_season_averages = data_season_averages['data'][0].keys()
                    writer_season_averages = csv.DictWriter(csvfile, fieldnames=fieldnames_season_averages)
                    writer_season_averages.writeheader()

            # Write season averages data to CSV file
            write_season_averages_data(data_season_averages['data'])

            # Increment the request counter
            request_counter_season_averages += 1

            # Check if there are more pages
            if 'next_page' in data_season_averages['meta'] and data_season_averages['meta']['next_page'] is not None:
                # Update the page parameter for the next request
                params_season_averages['page'] = data_season_averages['meta']['next_page']
            else:
                # Break the loop if there are no more pages
                break
        else:
            print("No 'meta' key in the API response for season averages.")
            break
    else:
        # Break the loop if the request fails even after retries
        break

    print(f"Season averages data successfully retrieved from page {params_season_averages.get('page')} of {total_pages_season_averages} pages.")

print(f"All season averages data for the season {desired_season} successfully written to {csv_filename_season_averages}")
