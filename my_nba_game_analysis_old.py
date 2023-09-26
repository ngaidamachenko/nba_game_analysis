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
        #print(AWAY_TEAM)
        '''main_player_match = re.search(r'(\b[A-Z]\W\s[A-Z][a-z]+\b)', DESCRIPTION)#((\b[A-Z]\W\s[A-Z][a-z]+\b)\s)|
        if main_player_match:
            main_player = main_player_match[0]
        else:
            continue
        print(main_player)'''
        '''three_pts_regex = re.compile(r'(.*)makes 3-pt jump shot from')
        three_pts = three_pts_regex.search(DESCRIPTION)
        player_name = three_pts[1]'''
        if away_team_bool(AWAY_TEAM, CURRENT_TEAM):
            relevant_team = "away_team"
        else:
            relevant_team = "home_team"
        #search for stats in the description using patterns 
        for stat, pattern in player_data_patterns.items(): #items() retrieves stat-value pairs (stat: value)
            match = re.search(pattern, DESCRIPTION)
            if match:
                player_name = match.group(1)#first group match in regex 
                print(player_name)
                '''if stat not in game_summary[relevant_team]["players_data"][player_name][stat]:
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
        
        if away_team_bool(AWAY_TEAM, RELEVANT_TEAM):
            game_summary["away team"]["players_data"][player_name]['3P'] += 1
        else:
            game_summary["home team"]["players_data"][player_name]['3P'] += 1
        break
        print(three_pts[1])'''
    ''' #DATA will be an array of hashes with this format:
    #DUNE - PART II
        PLAYER_DATA = {"player_name": XXX, "FG": XXX, "FGA": XXX, "FG%": XXX, "3P": XXX, "3PA": XXX, "3P%": XXX, "FT": XXX, "FTA": XXX, "FT%": XXX, "ORB": XXX, "DRB": XXX, "TRB": XXX, "AST": XXX, "STL": XXX, "BLK": XXX, "TOV": XXX, "PF": XXX, "PTS": XXX}
        DATA_HEADER = "\t".join(["player_name", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"])
        #return game_summary
        DATA = DATA_HEADER.append(PLAYER_DATA)
        #regex_main_name = #regex mainname = ((\b[A-Z]\W\s[A-Z][a-z]+\b)\s)|(\b[A-Z]\W\s[A-Z][a-z]+\b)\( to search for a name followed by spacebar or '(' - main player's name
                        #regex supportname = (\b[A-Z]\W\s[A-Z][a-z]+\b)\)
   # regex_fg
   # regex_fga
        FGA_percent = FG/FGA
        three_pts_percent = three_pts/three_pts_attempt
        free_throw_percent = free_throw/free_flow_attempt
        TRB = ORB+DRB'''

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