import requests

#get all players
url = "https://www.balldontlie.io/api/v1/players"
params= {
    "page" : 1,
    "per_page" : 100,
    "search" : "jayson tatum"
}
all_players = requests.get(url, params=params).json()

#get a specific player

url = "https://www.balldontlie.io/api/v1/players/237"
specific_player = requests.get(url).json()

#get a specific game

url = "https://www.balldontlie.io/api/v1/games"
params= {
    "page" : 1,
    "per_page" : 100,
    "seasons" : [2018, 2019, 2020, 2021, 2022, 2023]
}
specific_game = requests.get(url, params=params).json()

#get all stats
url = "https://www.balldontlie.io/api/v1/stats"
params= {
    "page" : 1,
    "per_page" : 100,
    "seasons" : [2018, 2019, 2020, 2021, 2022, 2023],
    "player_ids": 434
}
all_stats = requests.get(url, params=params).json()
print(all_stats)
