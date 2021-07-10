import json

with open("anime_key_users_value1.json") as f:
    anime_table = json.load(f)

with open("users_key_anime_value1.json") as f:
    user_table = json.load(f)

def find_similar_users(user_id):
    animes_watched = user_table[user_id]
    similar_users = []
    for i in animes_watched:
        if str(i) in anime_table:
            similar_users += anime_table[str(i)]
##        else:
##            print("doesn't exist")
    user_prevelence = {i : 0 for i in similar_users}
    for i in similar_users:
        user_prevelence[i] += 1
    user_prevelence = [(i, user_prevelence[i]) for i in user_prevelence]
    user_prevelence.sort(reverse = True, key = lambda x : x[1])
    print(user_prevelence)
    
def find_similar_animes(user_id, user_prevelence):
    # get closest user
    curr_neighbor = user_prevelence[0][0]
    result = None
    # while we haven't found a good anime
    while not result:
        # get all the animes of this new user
        curr_animes = user_table[curr_neighbor]
        # iterate through all the animes
        for i in curr_animes:
            # if I haven't watched this
            if i not in user_table[i]:
                return i
    return 1
