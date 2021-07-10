from flask import *
import cluster
app = Flask(__name__)

with open("anime_name_key_anime_id_value1.json") as f:
    anime_names = json.loads(f.read())

with open("anime_id_key_anime_name_value.json") as f:
    anime_id_to_names = json.loads(f.read())
history = []



@app.route("/", methods = ["GET", "POST"])
@app.route("/home/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        anime_name = request.form["anime-name"]

        if anime_name not in anime_names.keys():
            output = "not know anime"
            #return or something
        else:
            history.append(anime_names[anime_name])
            user_prevelence = cluster.find_similar_users(animes_watched=history)
            similar_anime_id = cluster.find_similar_animes(history, user_prevelence)
            similar_anime_name = anime_id_to_names[str(similar_anime_id)]
            output = similar_anime_name
            return render_template("index.html", suggested_name=output)

    return render_template("index.html")


#Borrowed from https://gist.github.com/itsnauman/b3d386e4cecf97d59c94
@app.context_processor
def override_url_for():
    return dict(url_for = dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == "static":
        filename = values.get('filename', None)
        if filename:
            path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == "__main__":
    #app.run(host='localhost', debug=False, port=8000, threaded=True)
    app.run(debug=True)