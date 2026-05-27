# Testing area
import json
import requests
"""
header = {'User-Agent': 'chesstats-app (your@email.com)'}
response = requests.get("https://api.chess.com/pub/player/kubson_alc/games/2026/05", headers=header, timeout=5)

parsed = response.json()

print(json.dumps(parsed, indent=4))
"""

def processed_opening_name(opening_url: str):
    raw_name = opening_url.split('/')[-1]
    words_list = raw_name.split('-')
    return " ".join(words_list)