import json
with open("users_key_anime_value1.json") as f:
    data = json.load(f)
    print(data["5])

    


def find_similar_users(user_id):
    animes_watched = user_table[user_id]
    similar_users = []
    for i in animes_watched:
        similar_users += anime_table[i]
    user_prevelence = {i : 0 for i in similar_users}
    for i in similar_users:
        user_prevelence[i] += 1
    user_prevelence = [(i, user_prevelence[i]) for i in user_prevelence]
    user_prevelence.sort(reverse = True, key = lambda x : x[1])
    print(user_prevelence)
    
    
