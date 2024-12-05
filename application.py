import json

from flask import Flask, jsonify, request
from flask_cors import CORS

from app.analysis.fantasy_league_analysis.league import League
from app.analysis.fantasy_league_analysis.export import export_league, export_team


def handler(event, context):
    event_body = json.loads(event["body"])
    if event_body["method"] == "league-analysis":
        return json.dumps(handle_league_analysis(event_body))

    if event_body["method"] == "wakeup-league-analysis":
        print("Received wakeup")
        return json.dumps({})


def handle_league_analysis(event_body):
    print("Received request for league analysis")
    try:
        # Argument reqs
        # ESPN: sport, leagueId, year, (espnS2, for private leagues)
        # Sleeper: leagueId, year
        league = League(event_body)
        league_export = {
            "league": export_league(league),
            "teams": [export_team(team) for team in league.teams],
        }
    except Exception as e:
        print(str(e))
        return {"errorMessage": str(e)}

    return league_export

# for local testing
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def post_data():
    data = request.json
    response = handle_league_analysis(data)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
