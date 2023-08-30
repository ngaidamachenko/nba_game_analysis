import csv
import re

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

    game_summary = {"home_team": {"name": HOME_TEAM, "players_data": DATA}, "away_team": {"name": AWAY_TEAM, "players_data": DATA}}
    #DATA will be an array of hashes with this format:
    DATA = {"player_name": XXX, "FG": XXX, "FGA": XXX, "FG%": XXX, "3P": XXX, "3PA": XXX, "3P%": XXX, "FT": XXX, "FTA": XXX, "FT%": XXX, "ORB": XXX, "DRB": XXX, "TRB": XXX, "AST": XXX, "STL": XXX, "BLK": XXX, "TOV": XXX, "PF": XXX, "PTS": XXX}
    DATA_HEADER = "\t".join(["player_name", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"])
    #return game_summary
def _main():
    play_by_play_moves = load_data("nba_game_blazers_lakers_20181018.txt")
    analyse_nba_game(play_by_play_moves)

_main()

#DUNE - PART II

"""
    FG: Field Goals Made
    FGA: Field Goal Attempts
    FG%: Field Goal Percentage
    3P: Three-Pointers Made
    3PA: Three-Point Attempts
    3P%: Three-Point Percentage
    FT: Free Throws Made
    FTA: Free Throw Attempts
    FT%: Free Throw Percentage
    ORB: Offensive Rebounds
    DRB: Defensive Rebounds
    TRB: Total Rebounds
    AST: Assists
    STL: Steals
    BLK: Blocks
    TOV: Turnovers
    PF: Personal Fouls
    PTS: Points
"""