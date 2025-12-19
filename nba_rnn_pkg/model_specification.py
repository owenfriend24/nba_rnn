import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.preprocessing.sequence import pad_sequences

def prepare_rnn_dataframe(df, features, targets, binaries, metadata):
    df['gameDate'] = pd.to_datetime(df['gameDate'])
    df = df.sort_values(['personId', 'gameDate']).reset_index(drop=True)

    # 1. create target columns (the next game for any given game)
    new_target_names = [f"NEXT_{col}" for col in targets]
    df[new_target_names] = df.groupby('personId')[targets].shift(-1)

    # 2. scale inputs
    continuous_features = [col for col in features if col not in binaries]
    x_scaler = StandardScaler()
    df[continuous_features] = x_scaler.fit_transform(df[continuous_features])
    
    # 3. scale targets
    # KEEP 'NEXT_win' as raw 0/1
    stats_to_scale = [col for col in new_target_names if 'win' not in col]
    y_scaler = StandardScaler()
    df[stats_to_scale] = y_scaler.fit_transform(df[stats_to_scale])

    # 4. drop the last game of the season (since no 'next game' exists to predict)
    df = df.dropna(subset=new_target_names)

    return df, x_scaler, y_scaler, new_target_names

def create_3d_arrays(df, feature_cols, binary_cols, target_cols):
    X_list = []
    Y_list = []
    player_ids = []

    # combine scaled features and binary features for the input
    all_input_cols = feature_cols + binary_cols
    
    # group by player to isolate their season sequence
    for pid, group in df.groupby('personId'):
        # 1. extract the sequential data for this player
        # shape: (Games_Played, Features)
        x_player = group[all_input_cols].values
        y_player = group[target_cols].values
        
        X_list.append(x_player)
        Y_list.append(y_player)
        player_ids.append(pid) # keep track of which row is which player

    # 2. padding
    # since not all players played 82 games, we pad the sequences with zeros 
    # at the beginning ('pre') so the most recent games are at the end
    X_3D = pad_sequences(X_list, padding='pre', dtype='float32')
    Y_3D = pad_sequences(Y_list, padding='pre', dtype='float32')
    
    return X_3D, Y_3D, player_ids