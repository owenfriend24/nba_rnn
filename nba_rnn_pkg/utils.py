import kagglehub
import os
import pandas as pd
import numpy as np


def pull_season_data(season_start, season_end):
    season_start = pd.to_datetime(season_start).date()
    season_end = pd.to_datetime(season_end).date()
    
    path = kagglehub.dataset_download("eoinamoore/historical-nba-data-and-player-box-scores")
    player_stats = pd.read_csv(f'{path}/PlayerStatistics.csv', low_memory = False)
    kee
    # base player stats
    player_stats['gameDateTimeEst'] = (pd.to_datetime(player_stats['gameDateTimeEst'], format='mixed', utc=True).dt.tz_convert('US/Eastern'))
    player_stats['gameDate'] = player_stats['gameDateTimeEst'].dt.date

    # add relevant team stats for advanced stats
    team_stats = pd.read_csv(f'{path}/TeamStatistics.csv')
    team_stats['gameDateTimeEst'] = (pd.to_datetime(team_stats['gameDateTimeEst'], format='mixed', utc=True).dt.tz_convert('US/Eastern'))
    team_stats['gameDate'] = team_stats['gameDateTimeEst'].dt.date
    team_stats = team_stats.rename(columns = {'teamName':'playerteamName', 'fieldGoalsAttempted':'teamFGA', 
                                          'freeThrowsAttempted':'teamFTA', 'turnovers':'teamTurnovers', 'numMinutes':'teamMinutes'})
    team_cols = ['gameId', 'playerteamName', 'teamFGA', 'teamFTA', 'teamTurnovers', 'teamMinutes']
    merged_df = pd.merge(player_stats, team_stats[team_cols], on=['gameId', 'playerteamName'], how='left')
        
    cleaned_df = merged_df[(merged_df['gameDate'] >= season_start) & (merged_df['gameDate'] <= season_end)]
    cleaned_df = cleaned_df.copy()
    cleaned_df['playerName'] = cleaned_df['firstName'] + ' ' + cleaned_df['lastName']

    return cleaned_df

def filter_season_data(df, min_games_played, min_minutes_per_game):
    by_player = df.groupby('personId')['numMinutes'].agg(['count', 'mean'])
    valid_players = by_player[(by_player['count'] >= min_games_played) & (by_player['mean'] >= min_minutes_per_game)].index
    cleaned_df = df[df['personId'].isin(valid_players)]
    return cleaned_df


def add_advanced_stats(df):
    df = df.copy()
    # 1. True Shooting Percentage (Efficiency)
    # Formula: PTS / (2 * (FGA + 0.44 * FTA))
    df['trueShooting'] = df['points'] / (2 * (df['fieldGoalsAttempted'] + (0.44 * df['freeThrowsAttempted'])))
    
    # 2. Usage Rate (estimate of plays 'used' while on floor)
    # captures how much of the team's offense goes through each player
    num = (df['fieldGoalsAttempted'] + 0.44 * df['freeThrowsAttempted'] 
           + df['turnovers']) * (df['teamTurnovers'] / 5)
    
    den = df['numMinutes'] * (df['teamFGA'] + 0.44 * df['teamFTA'] + df['teamTurnovers'])
    df['usageRate'] = 100 * (num / den)
    
    # 3. Game Score (John Hollinger's metric for single-game productivity)
    df['gameScore'] = (df['points'] + 0.7 * df['reboundsOffensive'] + 0.3 
                           * df['reboundsDefensive'] + df['steals'] + 
                  0.7 * df['assists'] + 0.7 * df['blocks'] - 0.4 * df['fieldGoalsAttempted'] - 
                  0.7 * df['freeThrowsAttempted'] - df['turnovers'])
    
    # 4. Assist-to-Turnover Ratio (Playmaking security)
    df['assistTurnoverRatio'] = df['assists'] / df['turnovers'].replace(0, 1)

    return df


def clean_master_data(df):
    return df[['personId', 'playerName', 'gameId', 'gameDate', 'win', 'home', 'numMinutes', 'points', 'assists',
       'blocks', 'steals', 'fieldGoalsAttempted', 'fieldGoalsMade',
       'fieldGoalsPercentage', 'threePointersAttempted', 'threePointersMade',
       'threePointersPercentage', 'freeThrowsAttempted', 'freeThrowsMade',
       'freeThrowsPercentage', 'reboundsDefensive', 'reboundsOffensive',
       'reboundsTotal', 'foulsPersonal', 'turnovers', 'plusMinusPoints',
                   'trueShooting', 'usageRate', 'gameScore', 'assistTurnoverRatio']]

    


    