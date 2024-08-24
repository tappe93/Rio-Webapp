from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

seasons = {
    "season-df-4":"Dragonflight Season 4",
    "season-df-3":"Dragonflight Season 3",
    "season-df-2":"Dragonflight Season 2",
    "season-df-1":"Dragonflight Season 1",
    "season-sl-4":"Shadowlands Season 4",
    "season-sl-3":"Shadowlands Season 3",
    "season-sl-2":"Shadowlands Season 2",
    "season-sl-1":"Shadowlands Season 1",
    "season-bfa-4":"Battle for Azeroth Season 4",
    "season-bfa-3":"Battle for Azeroth Season 3",
    "season-bfa-2":"Battle for Azeroth Season 2",
    "season-bfa-1":"Battle for Azeroth Season 1",
}


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        rio_data = request.form.get("url").split("/")
        region = rio_data[-3]
        realm = rio_data[-2]
        character = rio_data[-1]
        if region and realm and character:
            return redirect(url_for('character_page',region=region, realm=realm, character=character))
        else:
            return render_template("index.html", error = "Invalid Raider.io url")
        #
                
    return render_template("index.html")#, data=data, error=error, selected_seasons=seasons)

@app.route("/<region>/<realm>/<character>", methods=["GET"])
def character_page(region, realm, character):
    try:
        data = fetch_raiderio_data(region,realm, character,seasons)
        return render_template("results.html", region=region.upper(), realm=realm.capitalize(), character=character.capitalize(), data=data)
    except Exception as e:
        return render_template("error.html", error=str(e))    

def fetch_raiderio_data(region,realm, character, selected_seasons):
    url = f"https://raider.io/api/v1/characters/profile?region={region}&realm={realm}&name={character}&fields=mythic_plus_scores_by_season"
    for season in list(selected_seasons.keys()):
        url += "%3A"+season#season-df-4%3Aseason-df-3%3Aseason-df-2%3Aseason-df-1%3Aseason-sl-4%3Aseason-sl-3"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        scores = []
        for season_data in data.get('mythic_plus_scores_by_season', []):
            season = season_data['season']
            score = season_data['scores']['all']
            scores.append({'season': seasons[season], 'score': score})
        return scores
    return None

if __name__ == "__main__":
    app.run(debug=True)
