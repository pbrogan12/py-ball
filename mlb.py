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

    for game in data['data']['games']['game']:
        homeTeamName = game['home_team_name']
        awayTeamName = game['away_team_name']
        try:
            homeTeamScore = game['linescore']['r']['home']
            awayTeamScore = game['linescore']['r']['away']
            inning = game['status']['inning_state'] + ' ' + game['status']['inning']
        except:
            homeTeamScore = ''
            awayTeamScore = ''
            inning = game['time_hm_lg']

        msg = awayTeamName + ' ' + awayTeamScore + ' ' + homeTeamName + ' ' + homeTeamScore + ' ' + inning
        print msg

def get_leaders(limit='10', stat='h', year=time.strftime('%Y')):
    url = "http://mlb.mlb.com/pubajax/wf/flow/stats.splayer?season={0}&sort_order='desc'&sort_column='{2}'&stat_type=hitting&page_type=SortablePlayer&game_type='R'&player_pool=QUALIFIER&season_type=ANY&sport_code='mlb'&results={1}&recSP=1&recPP=10".format(year,limit,stat)
    data = requests.get(url)
    data = data.json()
    for player in data['stats_sortable_player']['queryResults']['row']:
        print player['name_display_first_last'] ,player['player_id'], player['team'], player['bats'], player['h'], player['avg']

if __name__ == '__main__':
    get_scores()
