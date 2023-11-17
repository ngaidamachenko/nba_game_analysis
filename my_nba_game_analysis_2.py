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

def away_team_bool(AWAY_TEAM, CURRENT_TEAM):
    return AWAY_TEAM == CURRENT_TEAM

def analyse_nba_game(play_by_play_moves):
    game_summary = {"home_team": {"name": "", "players_data": {}}, "away_team": {"name": "otherteam", "players_data": {}}}
    
    player_data_patterns = {#dictionary to store stats search patterns
        "FG": r'(.*) makes (2-pt|3-pt) jump shot from',
        "FGA": r'(.*) (makes|misses) (2-pt|3-pt) jump shot from', #made+attempts?
        #"FG%": #fg/fga,
        "3P": r'(.*)makes 3-pt jump shot from',
        "3PA": r'(.*) (makes|misses) (3-pt) jump shot from',
        #"3P%": #3p/3pa,
        "FT": r'(.*) makes free throw',
        "FTA": r'(.*) (makes|misses) free throw',
        #"FT%": #ft/fta,
        "ORB": r'Offensive rebound by (\b[A-Z]\W\s[A-Z][a-z]+\b)',
        "DRB": r'Defensive rebound by (\b[A-Z]\W\s[A-Z][a-z]+\b)',
        "TRB": r'Defensive rebound by (\b[A-Z]\W\s[A-Z][a-z]+\b)' or r'Offensive rebound by (\b[A-Z]\W\s[A-Z][a-z]+\b)',
        "AST": r'assist by (\b[A-Z]\W\s[A-Z][a-z]+\b)',
        "STL": r'steal by (\b[A-Z]\W\s[A-Z][a-z]+\b)',
        "BLK": r'block by (\b[A-Z]\W\s[A-Z][a-z]+\b)' ,
        "TOV": r'Turnover by (\b[A-Z]\W\s[A-Z][a-z]+\b)',
        "PF": r'foul by (\b[A-Z]\W\s[A-Z][a-z]+\b)',
       # "PTS": #add 2pts|1pt|3pts,
    }

    for play in play_by_play_moves:
      # values = play_by_play_moves.split('|')
        
        #PERIOD = play[0]
        #REMAINING_SEC = play[1]
        CURRENT_TEAM = play[2]
        AWAY_TEAM = play[3]
        HOME_TEAM = play[4]
        #AWAY_SCORE = play[5]
        #HOME_SCORE = play[6]
        DESCRIPTION = play[7]
        #print(AWAY_TEAM)'
        #player_name = None
        if away_team_bool(AWAY_TEAM, CURRENT_TEAM):
            relevant_team = "away_team"
        else:
            relevant_team = "home_team"
        
        #player_name = None
        #search for stats in the description using patterns 
        for stat, pattern in player_data_patterns.items(): #items() retrieves stat-value pairs (stat: value)
            match = re.search(pattern, DESCRIPTION)
            if match:
                player_name = match.group(1)#first group match in regex 
                #print(player_name)
                if player_name not in game_summary[relevant_team]["players_data"]:
                    game_summary[relevant_team]["players_data"][player_name] = {
                    "Players": player_name,
                    "FG": 0,
                    "FGA": 0,
                    "3P": 0,
                    "3PA": 0,
                    "FT": 0,
                    "FTA": 0,
                    "ORB": 0,
                    "DRB": 0,
                    "TRB": 0,
                    "AST": 0,
                    "STL": 0,
                    "BLK": 0,
                    "TOV": 0,
                    "PF": 0,
                }
                if stat not in game_summary[relevant_team]["players_data"][player_name]:
                    game_summary[relevant_team]["players_data"][player_name][stat] = 0 #initialize to 0
                else: 
                    game_summary[relevant_team]["players_data"][player_name][stat] += 1
        #manually calculate % stats and pts
    for team in game_summary:
        for player, stat in game_summary[team]["players_data"][player_name].items():
            FG = stat["FG"]
            FGA = stat["FGA"]
            FGP = FG/FGA
            print(FGP)
            stat["FG%"] = FGP

            three_pts_made = stat["3P"]
            three_pts_attempts = stat["3PA"] 
            three_pts_percentage = three_pts_made/three_pts_attempts
            print(three_pts_percentage) 
            stat["3P%"] = three_pts_percentage 

            FT = stat["FT"]
            FTA = stat["FTA"]
            FTP = FT/FTA
            print(FTP)
            stat["FTP"] = FTP

            PTS = 2*FG + 3*three_pts_made + FT
            print(PTS)

    return game_summary
    print(game_summary)
#DUNE - PART II
def print_nba_game_stats(game_summary):
    header = "\t".join(["Players", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"])
    print(header)
    
    '''#DATA will be an array of hashes with this format:
    
        PLAYER_DATA = {"player_name": XXX, "FG": XXX, "FGA": XXX, "FG%": XXX, "3P": XXX, "3PA": XXX, "3P%": XXX, "FT": XXX, "FTA": XXX, "FT%": XXX, "ORB": XXX, "DRB": XXX, "TRB": XXX, "AST": XXX, "STL": XXX, "BLK": XXX, "TOV": XXX, "PF": XXX, "PTS": XXX}
        
        #return game_summary
        DATA = DATA_HEADER.append(PLAYER_DATA)'''

def _main():
    play_by_play_moves = load_data("nba_game_blazers_lakers_20181018.txt")
    analyse_nba_game(play_by_play_moves)

_main()


#ABBREVIATIONS
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