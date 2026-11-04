import base64
import os
import requests
import datetime as dt
from xml.etree import ElementTree as ET
# import pprint


pull_games_url = "https://www.mysportsfeeds.com/api/feed/pull/mlb/current/game_startinglineup.xml"
username = os.environ.get("MYSPORTSFEEDS_USERNAME", "")
password = os.environ.get("MYSPORTSFEEDS_PASSWORD", "")
today_date = dt.date.today().strftime("%Y%m%d")

namespaces = {'gam': 'http://leaguemanager.beacontender.com/plugin/feed/gamestartinglineup',
                  'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

AL_teams = ['HOU', 'NYY', 'BAL', 'MIN', 'BOS', 'TEX', 'CLE', 'DET', 'LAA', 'TB', 'SEA', 'OAK', 'CWS', 'TOR', 'KC']


def send_lineups_request(away_team, home_team):

    fname = "lineups.xml"

    try:
        response = requests.get(
            url=pull_games_url,
            params={
                "gameid": today_date + "-" + away_team + "-" + home_team
            },
            headers={
                "Authorization": "Basic " + base64.b64encode(username + ":" + password)
            }
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        # print('Response HTTP Response Body: {content}'.format(
        #    content=response.content))
        with open(fname, 'wb') as f:
            f.write(response.text)
            f.close()

        away_pitcher_id, home_pitcher_id, away_lineup, home_lineup = extract_lineups(home_team)
        return int(away_pitcher_id), int(home_pitcher_id), away_lineup, home_lineup

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def extract_lineups(home_team):
    home_lineup = []
    away_lineup = []

    root = ET.parse('lineups.xml').getroot()
    teamlineup = root.findall('gam:teamLineup', namespaces)

    for t, team in enumerate(teamlineup):
        players = team.findall('./gam:expected/gam:starter/gam:player', namespaces)
        for player in players:
            if player.find('gam:ID', namespaces) is not None:
                if t == 0:
                    if player.find('gam:Position', namespaces).text == 'P':
                        away_pitcher = player.find('gam:ID', namespaces).text
                    if not (player.find('gam:Position', namespaces).text == 'P') & (home_team in AL_teams):
                        away_lineup.append(int(player.find('gam:ID', namespaces).text))
                    # print(player.find('gam:LastName', namespaces).text)
                elif t == 1:
                    if player.find('gam:Position', namespaces).text == 'P':
                        home_pitcher = player.find('gam:ID', namespaces).text
                    if not (player.find('gam:Position', namespaces).text == 'P') & (home_team in AL_teams):
                        home_lineup.append(int(player.find('gam:ID', namespaces).text))
                    # print(player.find('gam:LastName', namespaces).text)

    return away_pitcher, home_pitcher, away_lineup, home_lineup


# send_lineups_request("BOS", "BAL")
# extract_lineups("BAL")
