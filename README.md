# Welcome to My Nba Game Analysis
******************************************************************

## Task
The task is to analyze NBA game data and generate statistics for each player and team involved in the game. 

The challenge involves parsing the play-by-play moves, extracting relevant information, 
and summarizing player and team statistics accurately.

## Description
The project involves analyzing play-by-play data from an NBA game, extracting details about player actions (such as field goals, assists, rebounds, turnovers, etc.), 
and aggregating this data to produce comprehensive statistics for each player and team. 
The data is processed using Python with regular expressions to identify and parse specific actions in the game.

The end result looks like this: 

Players	FG	FGA	FG%	3P	3PA	3P%	FT	FTA	FT%	ORB	DRB	TRB	AST	STL	BLK	TOV	PF	PTS
Kevin Durant	9	21	.429	0	5	.000	9	10	.900	1	7	8	6	1	1	3	4	27
Stephen Curry	11	20	.550	5	9	.556	5	5	1.000	0	8	8	9	1	0	3	4	32
Klay Thompson	5	20	.250	1	8	.125	3	3	1.000	1	3	4	0	0	0	2	3	14
Draymond Green	1	6	.167	0	1	.000	0	0		1	12	13	5	3	0	6	3	2
Damian Jones	6	7	.857	0	0		0	0		2	1	3	2	0	3	2	4	12
Kevon Looney	5	11	.455	0	0		0	0		8	2	10	2	1	2	1	4	10
Shaun Livingston	3	5	.600	0	0		0	0		2	1	3	1	1	0	1	2	6
Quinn Cook	1	2	.500	1	1	1.000	0	0		1	1	2	1	0	0	2	2	3
Andre Iguodala	1	2	.500	0	1	.000	0	0		0	2	2	2	0	0	0	0	2
Jordan Bell	0	0		0	0		0	0		1	1	2	0	0	1	0	1	0
Jonas Jerebko	0	0		0	0		0	0		0	3	3	0	0	0	1	2	0	0
Alfonzo McKinnie	0	1	.000	0	1	.000	0	0		0	0	0	0	0	0	0	0	0
Team Totals	42	95	.442	7	26	.269	17	18	.944	17	41	58	28	7	7	21	29	108

## Installation
No installation need. Just clone the repository

## Usage
To install and run the project, follow these steps:
1. Clone the repository
2. In main: play_by_play_moves = load_data("nba_game_blazers_lakers_20181018.txt") enter *.txt file with the play by play moves summary.
   Each play follow this format:
   
   PERIOD|REMAINING_SEC|RELEVANT_TEAM|AWAY_TEAM|HOME_TEAM|AWAY_SCORE|HOME_SCORE|DESCRIPTION
3. Run the program using python my_nba_game_analysis.py

python my_nba_game_analysis.py
```

### The Core Team
Project completed by Nikita Gaidamachenko

<span><i>Made at <a href='https://qwasar.io'>Qwasar SV -- Software Engineering School</a></i></span>
<span><img alt='Qwasar SV -- Software Engineering School's Logo' src='https://storage.googleapis.com/qwasar-public/qwasar-logo_50x50.png' width='20px'></span>
