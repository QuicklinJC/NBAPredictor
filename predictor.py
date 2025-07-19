import numpy as np

def weighted_average(series, decay=0.85):
    """Weighted average: most recent has highest weight."""
    weights = np.array([decay ** i for i in range(len(series))])
    return np.average(series, weights=weights[::-1])

def predict_stats(gamelog_df):
    """
    Predicts player stats using weighted recent games,
    home/away adjustment, and (optionally) opponent defensive context.
    """
    stat_keys = {
        'PTS': 'Points',
        'AST': 'Assists',
        'REB': 'Rebounds',
        'STL': 'Steals',
        'BLK': 'Blocks',
        'FG3M': '3PM'
    }
    predictions = {}

    if 'MATCHUP' in gamelog_df.columns:
        # Home/Away boost (simple): +3% if home, -3% if away
        last_matchup = gamelog_df.iloc[0]['MATCHUP']
        is_home = 'vs.' in last_matchup
    else:
        is_home = True

    for k, label in stat_keys.items():
        if k in gamelog_df.columns:
            data = gamelog_df[k]
            pred = weighted_average(data)
            # Home/away adjust
            if is_home:
                pred *= 1.03
            else:
                pred *= 0.97
            predictions[label] = round(pred, 1)
        else:
            predictions[label] = None

    return predictions
