import requests
import time
import argparse
from prettytable import PrettyTable

# A function that returns scores on a certain day


def get_scores(date=None):
    if not date:
        date = time.strftime("%m/%d/%Y")

    try:
        date = time.strptime(date, "%m/%d/%Y")
    except:
        print "Date must be in MM/DD/YYYY format."
        raise

    url = 'http://mlb.mlb.com/gdcross/components/game/mlb/year_{0}/month_{1:02d}/day_{2:02d}/master_scoreboard.json'.format(
        date.tm_year,
        date.tm_mon,
        date.tm_mday)

    data = requests.get(url)
    # Initialize json
    data = data.json()
    games = {}

    for game in data['data']['games']['game']:
        homeTeamName = game['home_name_abbrev']
        awayTeamName = game['away_name_abbrev']
        try:
            homeTeamScore = game['linescore']['r']['home']
            awayTeamScore = game['linescore']['r']['away']
            inning = game['status']['inning_state'] + \
                ' ' + game['status']['inning']
        except:
            homeTeamScore = ''
            awayTeamScore = ''
            inning = game['time_hm_lg']

        games[awayTeamName + homeTeamName] = {
            'homeTeamName': homeTeamName,
            'awayTeamName': awayTeamName,
            'homeTeamScore': homeTeamScore,
            'awayTeamScore': awayTeamScore,
            'inning': inning
        }

    return games


def get_leaders(limit='10', stat='h', year=time.strftime('%Y')):
    playerDict = {}
    payload = {
        'season': year,
        'sort_order': '\'desc\'',
        'sort_column': '{}'.format(stat),
        'stat_type': 'hitting',
        'page_type': 'SortablePlayer',
        'game_type': '\'R\'',
        'player_pool': 'QUALIFIER',
        'season_type': 'ANY',
        'sport_code': '\'mlb\'',
        'results': limit,
        'recSP': '1',
        'recPP': '50'
    }
    url = 'http://mlb.mlb.com/pubajax/wf/flow/stats.splayer'
    data = requests.get(url, params=payload)
    data = data.json()
    for player in data['stats_sortable_player']['queryResults']['row']:
        playerDict[player['name_display_first_last']] = {}
        playerDict[
            player['name_display_first_last']]['playerId'] = player[
            'player_id']
        playerDict[player['name_display_first_last']]['team'] = player['team']
        playerDict[player['name_display_first_last']]['bats'] = player['bats']
        playerDict[player['name_display_first_last']]['h'] = player['h']
        playerDict[player['name_display_first_last']]['avg'] = player['avg']

    return playerDict


def get_recent(playerId, limit='10', stat='h'):
    payload = {
        'results': limit,
        'game_type': '\'R\'',
        'season': time.strftime('%Y'),
        'player_id': playerId,
        'mlb_individual_hitting_last_x_total.col_in': [
            'game_date',
            'opp',
            'ab',
            'r',
            'h',
            'hr',
            'rbi',
            'bb',
            'so',
            'sb',
            'avg',
            'home_away',
            'game_id',
            'game_type']}
    url = 'http://mlb.mlb.com/lookup/json/named.mlb_bio_hitting_last_10.bam'
    data = requests.get(url, params=payload)
    data = data.json()
    return data['mlb_bio_hitting_last_10'][
        'mlb_individual_hitting_last_x_total']['queryResults']['row'][stat]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--date', help='Date must be in DD/MM/YYYY')
    args = parser.parse_args()

    if args.date:
        scores = get_scores(date=args.date)

    else:
        scores = get_scores()

    table = PrettyTable(['Away', 'A Score', 'Home', 'H Score', 'Inning'])
    for i in scores:
        table.add_row([scores[i]['awayTeamName'],
                      scores[i]['awayTeamScore'],
                      scores[i]['homeTeamName'],
                      scores[i]['homeTeamScore'],
                      scores[i]['inning']])
    print table.get_string(sortby='Inning')
