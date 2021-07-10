DONE_PHRASES = ["d", "done"]

def is_finished(inp):
    if inp.lower() in DONE_PHRASES:
        return True

    return False

def get_input():
    anime_prompt = "Please enter the name of an anime you loved!\nEnter d, D or done if you want to view your recommendations."
    this_inp = input(anime_prompt)
    return this_inp

if __name__ == "__main__":
    history = []
    this_inp = get_input()

    while not is_finished(this_inp):
        history.append(this_inp)
        this_inp = get_input()
