import csv

#DUNE - PART I
def load_data(filename):
    result = []

    with open(filename,'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='|')

        fields = next(csvreader)

        for row in csvreader:
            result.append(row)
    return result

def analyse_nba_game(play_by_play_moves):
   # game_summary = {"home_team": {"name": TEAM_NAME, "players_data": DATA}, "away_team": {"name": TEAM_NAME, "players_data": DATA}}
    #DATA will be an array of hashes with this format:
    #{"player_name": XXX, "FG": XXX, "FGA": XXX, "FG%": XXX, "3P": XXX, "3PA": XXX, "3P%": XXX, "FT": XXX, "FTA": XXX, "FT%": XXX, "ORB": XXX, "DRB": XXX, "TRB": XXX, "AST": XXX, "STL": XXX, "BLK": XXX, "TOV": XXX, "PF": XXX, "PTS": XXX}

    for play in play_by_play_moves:
      # values = play_by_play_moves.split('|')
        PERIOD = play[0]
        REMAINING_SEC = play[1]
        RELEVANT_TEAM = play[2]
        AWAY_TEAM = play[3]
        HOME_TEAM = play[4]
        AWAY_SCORE = play[5]
        HOME_SCORE = play[6]
        DESCRIPTION = play[7]
        print(AWAY_TEAM)


    #return game_summary
def _main():
    play_by_play_moves = load_data("nba_game_blazers_lakers_20181018.txt")
    analyse_nba_game(play_by_play_moves)

_main()

#DUNE - PART II