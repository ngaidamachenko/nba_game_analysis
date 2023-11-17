import csv
import re

#Issue 1: some actions get attributed to the wrong team, but the right player
#Issue 2: thus players get duplicated on both sides
#Issue 3: Steph and Seth Curry merge into one player as both players appear as S. Curry 


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
        "FG": r"(.*) makes (2-pt|3-pt)",
        "FGA": r"(.*) (makes|misses) (2-pt|3-pt)",
        "3P": r"(.*) makes 3-pt jump shot from",
        "3PA": r"(.*) (makes|misses) (3-pt) jump shot from",
        "FT": r"(.*) makes (|clear path )free throw",
        "FTA": r"(.*) (makes|misses) (|clear path )free throw",
        "ORB": r"Offensive rebound by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)",
        "DRB": r"Defensive rebound by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)",
        "TRB": r"(Offensive|Defensive) rebound by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)",
        "AST": r"assist by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)",
        #"STL": r"steal by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)",
        "BLK": r"block by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)",
        "TOV": r"Turnover by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)",
        "PF": r"(Defensive|Offensive) foul by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)" #or r"Defensive foul by (\b[A-Z]\W\s[A-Z][a-z]+(?:-[A-Z][a-z]+)?\b)",
    }

    player_data_patterns_exceptions = {#for when CURRENT_TEAM for the player is the opposing team
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
            matches = re.finditer(pattern, DESCRIPTION)                  
            if away_team_bool(AWAY_TEAM, CURRENT_TEAM):
                relevant_team = "away_team"
                game_summary[relevant_team]["name"] = AWAY_TEAM
            else:
                relevant_team = "home_team"
                game_summary[relevant_team]["name"] = HOME_TEAM
            for match in matches:
                if stat == "TRB" or stat == "PF":
                    player_name = match.group(2)
                else:
                    player_name = match.group(1) #looks for the first group in regex pattern  
                if player_name not in game_summary[relevant_team]["players_data"]:
                    game_summary[relevant_team]["players_data"][player_name] = { #have to add +1 to the first stat encountered for that player in the same step
                        "player_name": player_name,
                        "FG": 0,
                        "FGA": 0,
                        "FG%": 0,
                        "3P": 0,
                        "3PA": 0,
                        "3P%": 0,
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

        for stat, pattern in player_data_patterns_exceptions.items(): #for outlier patterns
            match = re.search(pattern, DESCRIPTION)                  
            if away_team_bool(AWAY_TEAM, CURRENT_TEAM): #reversed
                relevant_team = "home_team"
                game_summary[relevant_team]["name"] = HOME_TEAM
            else:
                relevant_team = "away_team"
                game_summary[relevant_team]["name"] = AWAY_TEAM
            if match:
                player_name = match.group(1)  
                if player_name not in game_summary[relevant_team]["players_data"]:
                    game_summary[relevant_team]["players_data"][player_name] = {  #have to add +1 to the first stat encountered for that player in the same step
                        "player_name": player_name,
                        "FG": 0,
                        "FGA": 0,
                        "FG%": 0,
                        "3P": 0,
                        "3PA": 0,
                        "3P%": 0,
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
                else:
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
                stat["PTS"] = 2 * (stat["FG"] - stat["3P"]) + 3 * stat["3P"] + 1* stat["FT"] #FG - 3P to eliminate duplicate points
    #print(game_summary["home_team"])
    #print(game_summary)
    return game_summary

def print_nba_game_stats(team_data):
    header = "\t".join([
        "Players", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB",
        "AST", "STL", "BLK", "TOV", "PF", "PTS"
    ])
    print(header)

    team_totals = {
        "FG": 0, "FGA": 0, "FG%": 0, "3P": 0, "3PA": 0, "3P%": 0, "FT": 0, "FTA": 0,
        "FT%": 0, "ORB": 0, "DRB": 0, "TRB": 0, "AST": 0, "STL": 0, "BLK": 0,
        "TOV": 0, "PF": 0, "PTS": 0
    }
    
    total_count = {"FG%": 0, "3P%": 0, "FT%": 0}

    for player, stats in team_data["players_data"].items():
        line = "\t".join([
            player,
            str(stats.get("FG", 0)),
            str(stats.get("FGA", 0)),
            str(stats.get("FG%", 0)),
            str(stats.get("3P", 0)),
            str(stats.get("3PA", 0)),
            str(stats.get("3P%", 0)),
            str(stats.get("FT", 0)),
            str(stats.get("FTA", 0)),
            str(stats.get("FT%", 0)),
            str(stats.get("ORB", 0)),
            str(stats.get("DRB", 0)),
            str(stats.get("TRB", 0)),
            str(stats.get("AST", 0)),
            str(stats.get("STL", 0)),
            str(stats.get("BLK", 0)),
            str(stats.get("TOV", 0)),
            str(stats.get("PF", 0)),
            str(stats.get("PTS", 0))
        ])
        print(line)

        # Calculate team totals and count for averages
        for key, value in stats.items():
            if key in team_totals:
                try:
                    team_totals[key] += int(value)
                except ValueError:
                    team_totals[key] += float(value)
                    total_count[key] += 1
    
    # Calculate averages and print totals for the team
    totals_line = "\t".join([
        "Totals",
        str(team_totals.get("FG", 0)),
        str(team_totals.get("FGA", 0)),
        str(round(team_totals.get("FG%", 0) / total_count["FG%"], 3) if total_count["FG%"] > 0 else 0),
        str(team_totals.get("3P", 0)),
        str(team_totals.get("3PA", 0)),
        str(round(team_totals.get("3P%", 0) / total_count["3P%"], 3) if total_count["3P%"] > 0 else 0),
        str(team_totals.get("FT", 0)),
        str(team_totals.get("FTA", 0)),
        str(round(team_totals.get("FT%", 0) / total_count["FT%"], 3) if total_count["FT%"] > 0 else 0),
        str(team_totals.get("ORB", 0)),
        str(team_totals.get("DRB", 0)),
        str(team_totals.get("TRB", 0)),
        str(team_totals.get("AST", 0)),
        str(team_totals.get("STL", 0)),
        str(team_totals.get("BLK", 0)),
        str(team_totals.get("TOV", 0)),
        str(team_totals.get("PF", 0)),
        str(team_totals.get("PTS", 0)),
    ])
    print(totals_line)

def _main():
    play_by_play_moves = load_data("nba_game_warriors_thunder_20181016.txt")
    game_summary = analyse_nba_game(play_by_play_moves)
    #home_team = game_summary["home_team"]
    #away_team = game_summary["away_team"]
    print_nba_game_stats(game_summary["home_team"])
    
    print_nba_game_stats(game_summary["away_team"])
    
    
    
_main()
