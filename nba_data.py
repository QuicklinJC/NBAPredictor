from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog, leaguegamefinder
import pandas as pd

def get_player_id(player_name):
    """Find NBA player ID by name (partial matches allowed)."""
    matches = players.find_players_by_full_name(player_name)
    if not matches:
        raise ValueError(f"No player found for '{player_name}'")
    return matches[0]['id']

def get_recent_game_logs(player_id, season='2023-24', n=10):
    logs = playergamelog.PlayerGameLog(player_id=player_id, season=season)
    df = logs.get_data_frames()[0]
    return df.head(n)

def get_next_game_info(player_id):
    logs = playergamelog.PlayerGameLog(player_id=player_id, season='2023-24')
    df = logs.get_data_frames()[0]
    last_game = df.iloc[0]
    team_id = last_game['TEAM_ID']
    last_game_date = last_game['GAME_DATE']

    finder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id, season_nullable='2023-24')
    all_games = finder.get_data_frames()[0]
    next_games = all_games[all_games['GAME_DATE'] > last_game_date]
    if next_games.empty:
        return None
    next_game = next_games.iloc[0]
    return {
        'opponent': next_game['MATCHUP'],
        'date': next_game['GAME_DATE']
    }
