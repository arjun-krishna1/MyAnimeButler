import json

with open("anime_name_key_anime_id_value1.json") as f:
    anime_names = json.loads(f.read())

print(anime_names.keys())
