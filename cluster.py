import json
import time

with open("anime_key_users_value1.json") as f:
    anime_table = json.load(f)

with open("users_key_anime_value1.json") as f:
    user_table = json.load(f)

def find_similar_users(user_id = None, animes_watched = None):
    if not animes_watched:
        if user_id:
            animes_watched = user_table[user_id]
        else:
            print("You must enter either a user id or anime watched data")
            return 0
    similar_users = []
    for i in animes_watched:
        if str(i) in anime_table:
            similar_users += anime_table[str(i)]
    user_prevelence = {i : 0 for i in similar_users}
    for i in similar_users:
        user_prevelence[i] += 1
    user_prevelence = [(i, user_prevelence[i]) for i in user_prevelence]
    user_prevelence.sort(reverse = True, key = lambda x : x[1])
    return user_prevelence
    
def find_similar_animes(animes_watched, user_prevelence):
    # get closest users
    current_neighbours = []
    starter = user_prevelence[0][1]
    for i in user_prevelence:
        if i[1] == starter:
            current_neighbours.append(i[0])

    # get all the animes of this new user\
    similar_animes = []
    for i in current_neighbours:
        if str(i) in user_table.keys():
            similar_animes += user_table[str(i)]
    anime_prevelence = {i : 0 for i in similar_animes}
    for i in similar_animes:
        anime_prevelence[i] += 1
    anime_prevelence = [(i, anime_prevelence[i]) for i in anime_prevelence]
    anime_prevelence.sort(reverse=True, key = lambda x : x[1])
    return anime_prevelence[0][0]





if __name__ == "__main__":
    user_id = "76"
    user_prevelence = find_similar_users(user_id)
    print(find_similar_animes(user_table[user_id], user_prevelence))