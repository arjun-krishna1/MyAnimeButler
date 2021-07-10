import cluster
import json

DONE_PHRASES = ["d", "done"]

def is_finished(inp):
    if inp.lower() in DONE_PHRASES:
        return True

    return False

with open("anime_name_key_anime_id_value1.json") as f:
    anime_names = json.loads(f.read())

with open("anime_id_key_anime_name_value.json") as f:
    anime_id_to_names = json.loads(f.read())

def get_input():
    while True:
        anime_prompt = "Please enter the name of an anime you loved!\nEnter 'done' to view your recommendations: "
        this_inp = input(anime_prompt)
        if this_inp not in anime_names.keys():
            if is_finished(this_inp):
                return 0
            else:
                print("Sorry, that name was not found")
        else:
            return this_inp
        

if __name__ == "__main__":
    history = []
    while True:
        this_inp = get_input()
        if not this_inp:
            break
        history.append(this_inp)
    
    history = [anime_names[i] for i in history]
    user_prevelence = cluster.find_similar_users(animes_watched = history)
    similar_anime_id = cluster.find_similar_animes(history, user_prevelence)
    similar_anime_name = anime_id_to_names[str(similar_anime_id)]
    print(similar_anime_name)
    
    

    
