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
        "ORB": r'Offensive rebound by (.*)',
        "DRB": r'Defensive rebound by (.*)',
        "TRB": r'(Ofensive|Defensive) rebound by (.*)',
        "AST": r'assist by (.*)',
        "STL": r'steal by (.*)',
        "BLK": r'block by (.*)' ,
        "TOV": r'Turnover by (.*)',
        "PF": r'Shooting foul by (.*)',
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
      #  print(AWAY_TEAM)

        if away_team_bool(AWAY_TEAM, CURRENT_TEAM):
            relevant_team = "away_team"
        else:
            relevant_team = "home_team"
        
        
        if player_name not in game_summary[relevant_team]["players_data"][player_name]:
            game_summary[relevant_team]["players_data"][player_name] = {
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
        #search for stats in the description using patterns 
        for stat, pattern in player_data_patterns.items(): #items() retrieves stat-value pairs (stat: value)
            match = re.search(pattern, DESCRIPTION)
            if match:
                player_name = match.group(1)#first group match in regex 
                #print(player_name)
                if stat not in game_summary[relevant_team]["players_data"][player_name][stat]:
                    game_summary[relevant_team]["players_data"][player_name][stat] = 0 #initialize to 0
                else: 
                    game_summary[relevant_team]["players_data"][player_name][stat] += 1
        #manually calculate % stats and pts
    for team in game_summary:
        for player_name, player_stats in game_summary[team]["players_data"].items():
            FG = player_stats["FG"]
            FGA = player_stats["FGA"]
            if FGA > 0:
                FGP = FG / FGA
                player_stats["FG%"] = f"{FGP:.3f}"  # Format as a percentage with 3 decimal places

            three_pts_made = player_stats["3P"]
            three_pts_attempts = player_stats["3PA"]
            if three_pts_attempts > 0:
                three_pts_percentage = three_pts_made / three_pts_attempts
                player_stats["3P%"] = f"{three_pts_percentage:.3f}"  # Format as a percentage with 3 decimal places

            FT = player_stats["FT"]
            FTA = player_stats["FTA"]
            if FTA > 0:
                FTP = FT / FTA
                player_stats["FT%"] = f"{FTP:.3f}"  # Format as a percentage with 3 decimal places

            PTS = 2 * FG + 3 * three_pts_made + FT
            player_stats["PTS"] = PTS

    return game_summary
    print(game_summary)

def _main():
    play_by_play_moves = load_data("nba_game_blazers_lakers_20181018.txt")
    analyse_nba_game(play_by_play_moves)

_main()
