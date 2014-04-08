import requests
import time

# A function that returns scores on a certain day
def get_scores(date=time.strftime('%d/%m/%Y')):
    date = date.split("/")
    year = date[2]
    month = date[1]
    day = date[0]
    url = 'http://mlb.mlb.com/gdcross/components/game/mlb/year_{0}/month_{1}/day_{2}/master_scoreboard.json'.format(year,month,day)
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
            inning = game['status']['inning_state'] + ' ' + game['status']['inning']
        except:
            homeTeamScore = ''
            awayTeamScore = ''
            inning = game['time_hm_lg']

        games[game['game_media']['media']['title']] = {
            'homeTeamName' : homeTeamName,
            'awayTeamName' : awayTeamName,
            'homeTeamScore' : homeTeamScore,
            'awayTeamScore' : awayTeamScore,
            'inning' : str(inning)
        }

    return games

def get_leaders(limit='10', stat='h', year=time.strftime('%Y')):
    payload = {
            'season' : year,
            'sort_order' : '\'desc\'',
            'sort_column' : '{}'.format(stat),
            'stat_type' : 'hitting',
            'page_type' : 'SortablePlayer',
            'game_type' : '\'R\'',
            'player_pool' : 'QUALIFIER',
            'season_type' : 'ANY',
            'sport_code' : '\'mlb\'',
            'results' : limit,
            'recSP' : '1',
            'recPP': '50'
    }
    url = 'http://mlb.mlb.com/pubajax/wf/flow/stats.splayer'
    data = requests.get(url,params=payload)
    data = data.json()
    for player in data['stats_sortable_player']['queryResults']['row']:
        print player['name_display_first_last'] ,player['player_id'], player['team'], player['bats'], player['h'], player['avg']

def get_recent(playerId, limit='10',stat='h'):
    payload = {
            'results' : limit,
            'game_type' : '\'R\'',
            'season' : time.strftime('%Y'),
            'player_id' : playerId,
            'mlb_individual_hitting_last_x_total.col_in' : ['game_date','opp','ab','r','h','hr','rbi','bb','so','sb','avg','home_away','game_id','game_type']
    }
    url = 'http://mlb.mlb.com/lookup/json/named.mlb_bio_hitting_last_10.bam'
    data = requests.get(url,params=payload)
    data = data.json()
    return data['mlb_bio_hitting_last_10']['mlb_individual_hitting_last_x_total']['queryResults']['row'][stat]

if __name__ == '__main__':
    get_scores()
