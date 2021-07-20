from flask import *
import os
import cluster
from data import anime_choices

app = Flask(__name__)

with open("data/anime_name_key_anime_id_value1.json") as f:
    anime_names = json.loads(f.read())

with open("data/anime_id_key_anime_name_value.json") as f:
    anime_id_to_names = json.loads(f.read())
history = []

blacklist = []
suggested_anime = "Select an anime below for a new recommendation!"


@app.route("/home/<name>", methods=["GET"])
def add_anime(name):
    if request.method == "GET":
        anime_name = name
        if anime_name not in anime_choices:
            output = f"'{anime_name}' is unknown"
            # return or something
        else:
            anime_choices.remove(anime_name)
            history.append(anime_names[anime_name])
            user_prevelence = cluster.find_similar_users(animes_watched=history)
            similar_anime_id = cluster.find_similar_animes(history, user_prevelence, blacklist)
            similar_anime_name = anime_id_to_names[str(similar_anime_id)]
            global suggested_anime
            suggested_anime = similar_anime_name
    return redirect(url_for('index'))


@app.route("/", methods = ["GET", "POST"])
@app.route("/home/", methods = ["GET", "POST"])
def index():
    global suggested_anime
    if request.method == "POST":
        if "remove-anime-button" in request.form:
            blacklist.append(suggested_anime)
            if suggested_anime in anime_choices:
                anime_choices.remove(suggested_anime)
            user_prevelence = cluster.find_similar_users(animes_watched=history)
            if user_prevelence:
                similar_anime_id = cluster.find_similar_animes(history, user_prevelence, blacklist)
                similar_anime_name = anime_id_to_names[str(similar_anime_id)]
                suggested_anime = similar_anime_name
        return render_template("index.html", suggested_name=suggested_anime, dropdown_choices = anime_choices)

    return render_template("index.html",
                       dropdown_choices=anime_choices,
                       suggested_name=suggested_anime)


# Borrowed from https://gist.github.com/itsnauman/b3d386e4cecf97d59c94
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == "static":
        filename = values.get('filename', None)
        if filename:
            path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == "__main__":
    # app.run(host='localhost', debug=False, port=8000, threaded=True)
    app.run(debug=True)
