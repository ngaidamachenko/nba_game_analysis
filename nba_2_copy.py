import csv
import re

def load_data(filename):
    result = []

    with open(filename, "r", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter="|")

        fields = next(csvreader)

        for row in csvreader:
            result.append(row)
    return result

def away_team_bool(AWAY_TEAM, CURRENT_TEAM):
    return AWAY_TEAM == CURRENT_TEAM

def analyse_nba_game(play_by_play_moves):
    game_summary = {
        "home_team": {"name": "", "players_data": {}},
        "away_team": {"name": "", "players_data": {}},
    }
    #game_summary = {} #initialazing player data dictionaries
    
    player_data_patterns = {  
        "FG": r"(.*) makes (2-pt|3-pt) jump shot from",
        "FGA": r"(.*) (makes|misses) (2-pt|3-pt) jump shot from",
        "3P": r"(.*) makes 3-pt jump shot from",
        "3PA": r"(.*) (makes|misses) (3-pt) jump shot from",
        "FT": r"(.*) makes free throw",
        "FTA": r"(.*) (makes|misses) free throw",
        "ORB": r"Offensive rebound by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)",
        "DRB": r"Defensive rebound by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)",
        "TRB": r"Defensive rebound by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)"
        or r"Offensive rebound by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)",
        "AST": r"assist by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)",
        #"STL": r"steal by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)",
        "BLK": r"block by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)",
        "TOV": r"Turnover by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)",
        "PF": r"Offensive foul by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)" 
        or r"Defensive foul by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)",
    }

    player_data_patterns_exceptions = {
        "STL": r"steal by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)",
        "PF": r"Shooting foul by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)",
    }

    for play in play_by_play_moves:
        CURRENT_TEAM = play[2]
        AWAY_TEAM = play[3]
        HOME_TEAM = play[4]
        DESCRIPTION = play[7]
        
        player_name = ""
        
        for stat, pattern in player_data_patterns.items():
            match = re.search(pattern, DESCRIPTION)                  
            if away_team_bool(AWAY_TEAM, CURRENT_TEAM):
                relevant_team = "away_team"
                game_summary[relevant_team]["name"] = AWAY_TEAM
            else:
                relevant_team = "home_team"
                game_summary[relevant_team]["name"] = HOME_TEAM
            if match:
                player_name = match.group(1)  
                if player_name not in game_summary[relevant_team]["players_data"]:
                    game_summary[relevant_team]["players_data"][player_name] = {
                        "player_name": player_name,
                        "FG": 0,
                        "FGA": 0,
                        "3P": 0,
                        "3PA": 0,
                        "FG%": 0,
                        "FT": 0,
                        "FTA": 0,
                        "FT%": 0,
                        "ORB": 0,
                        "DRB": 0,
                        "TRB": 0,
                        "AST": 0,
                        "STL": 0,
                        "BLK": 0,
                        "TOV": 0,
                        "PF": 0,
                        "PTS": 0,
                    }
                # Check if it's a shooting foul and adjust the relevant team accordingly
                #STL & Shooting PF: attributed for the right player, but opposing team
                #TOV: same line as STL, but attributed to the correct team
                #if "Shooting foul" in DESCRIPTION:
                #    game_summary["home_team"]["players_data"][player_name]["PF"] += 1
                #elif "steal by" in DESCRIPTION:
                #    game_summary["home_team"]["players_data"][player_name]["STL"] += 1
                #else:
                game_summary[relevant_team]["players_data"][player_name][stat] += 1
        for stat, pattern in player_data_patterns_exceptions.items():
            match = re.search(pattern, DESCRIPTION)                  
            if away_team_bool(AWAY_TEAM, CURRENT_TEAM):
                relevant_team = "home_team"
                game_summary[relevant_team]["name"] = HOME_TEAM
            else:
                relevant_team = "away_team"
                game_summary[relevant_team]["name"] = AWAY_TEAM
            if match:
                player_name = match.group(1)  
                if player_name not in game_summary[relevant_team]["players_data"]:
                    game_summary[relevant_team]["players_data"][player_name] = {
                        "player_name": player_name,
                        "FG": 0,
                        "FGA": 0,
                        "3P": 0,
                        "3PA": 0,
                        "FG%": 0,
                        "FT": 0,
                        "FTA": 0,
                        "FT%": 0,
                        "ORB": 0,
                        "DRB": 0,
                        "TRB": 0,
                        "AST": 0,
                        "STL": 0,
                        "BLK": 0,
                        "TOV": 0,
                        "PF": 0,
                        "PTS": 0,
                    }
                game_summary[relevant_team]["players_data"][player_name][stat] += 1
    for relevant_team in game_summary:
        for player_name, stat in game_summary[relevant_team]["players_data"].items():
            #FG = stat["FG"]
            #FGA = stat["FGA"]
            if stat["FGA"] > 0:
                FGP = stat["FG"] / stat["FGA"]
                stat["FG%"] = f"{FGP:.3f}"  # Format as a percentage with 3 decimal places

            #three_pts_made = stat["3P"]
            #three_pts_attempts = stat["3PA"]
            if stat["3PA"] > 0:
                three_pts_percentage = stat["3P"] / stat["3PA"]
                stat["3P%"] = f"{three_pts_percentage:.3f}"  # Format as a percentage with 3 decimal places

            #FT = stat["FT"]
            #FTA = stat["FTA"]
            if stat["FTA"] > 0:
                FTP = stat["FT"] / stat["FTA"]
                stat["FT%"] = f"{FTP:.3f}"  # Format as a percentage with 3 decimal places
                stat["PTS"] = 2 * stat["FG"] + 3 * stat["3P"] + stat["FT"]
    print(game_summary["home_team"]["players_data"]["S. Curry"])
    return game_summary

def print_nba_game_stats(summary):
    header = "\t".join(
        [
            "Players",
            "FG",
            "FGA",
            "FG%",
            "3P",
            "3PA",
            "3P%",
            "FT",
            "FTA",
            "FT%",
            "ORB",
            "DRB",
            "TRB",
            "AST",
            "STL",
            "BLK",
            "TOV",
            "PF",
            "PTS",
        ]
    )
    team_dict = header.join(summary)
    print(team_dict)
    return team_dict
                
def _main():
    play_by_play_moves = load_data("nba_game_warriors_thunder_20181016_Curry.txt")
    analyse_nba_game(play_by_play_moves)
    #print_nba_game_stats(summary)


_main()