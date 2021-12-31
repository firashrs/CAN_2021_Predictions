import pandas as pd
import numpy as np
import math
import tensorflow as tf
print('..imported modules.')


model = tf.keras.models.load_model('model.h5')

print('..imported Model.')


adress_fifa_results = 'fifa_national_teams_matches_1992_2021.csv'
dataset = pd.read_csv(adress_fifa_results)
print('loaded data')

rank_date = dataset['date']
for i, rd in enumerate(rank_date):
    dataset['date'][i] = rd.split('-')[0]
print('formatted date')

home_scrore_mean = (np.array(dataset['home_score'])[:-1]).mean()  
away_scrore_mean = (np.array(dataset['away_score'])[:-1]).mean() 

 
def get_last_encounter(home, away, year=2021):
    scr_diff = 0
    scr_offset = -1
    h_team = ''
    a_team = ''
    for i in range(dataset.shape[0]-1, -1, -1):
        
        if int(year) >= int(dataset['date'][i]):
            h_team = str(dataset['home_team'][i])
            a_team = str(dataset['away_team'][i])
            if (h_team == home) and (a_team == away):
                if math.isnan(dataset['home_score'][i]) or math.isnan(dataset['away_score'][i]):
                    continue
                scr_diff = float(int(dataset['home_score'][i]) - int(dataset['away_score'][i]))
                scr_offset = float(min(int(dataset['home_score'][i]), int(dataset['away_score'][i])))
                return scr_diff, scr_offset
            
    return -1, -1






adress_caf_2022_dataset = 'caf_2021_dataset.csv'

caf_2022_dataset = pd.read_csv(adress_caf_2022_dataset, sep='\t', encoding='utf-8')


def get_team_data(name, year=2021):
    nbr_examples = 0
    i = 0
    while (i<caf_2022_dataset.shape[0]) and (caf_2022_dataset['team'][i] != name):
        i = i + 1
    if i >= caf_2022_dataset.shape[0]:
        return -1
        
    rank = caf_2022_dataset.iloc[i]['rank'] 
    games_total = caf_2022_dataset.iloc[i]['games_total'] 
    games_win = caf_2022_dataset.iloc[i]['games_win'] 
    games_loss = caf_2022_dataset.iloc[i]['games_loss'] 
    games_tie = caf_2022_dataset.iloc[i]['games_tie'] 
    games_goal_ratio = caf_2022_dataset.iloc[i]['games_goal_ratio']
    
    
    return rank, games_total, games_win, games_loss, games_tie, games_goal_ratio


def inference(home_team, away_team, tournament='Serious', i = 0):
    
    hrank, hgames_total, hgames_win, hgames_loss, hgames_tie, hgames_goal_ratio = get_team_data(home_team)
    arank, agames_total, agames_win, agames_loss, agames_tie, agames_goal_ratio = get_team_data(away_team)
    
    
    rank_diff = hrank - arank
    rank_offset = min(hrank, arank)
    friendly = 0.0
    serious = 1.0
    if tournament == 'Friendly':
        friendly = 1.0
        serious = 0.0
    
    
    last_game_score_diff, last_game_score_offset = get_last_encounter(home_team, away_team)
    
    games_total_dif = hgames_total - agames_total
    games_win_dif = hgames_win - agames_win
    games_loss_dif = hgames_loss - agames_loss
    games_tie_dif = hgames_tie - agames_tie
    games_goal_ratio_dif = hgames_goal_ratio - agames_goal_ratio
    
    
    if last_game_score_offset == -1:
        if i == 0:
            opposite = inference(away_team, home_team, tournament, 1 )
            return (opposite[1], opposite[0])
        return home_scrore_mean, home_scrore_mean
    
    
    testX = np.array([[rank_diff,
                       rank_offset,
                       friendly,
                       serious,
                       last_game_score_diff,
                       last_game_score_offset,
                       games_total_dif,
                       games_win_dif,
                       games_loss_dif,
                       games_tie_dif,
                       games_goal_ratio_dif]])
    
    predicted = model.predict_on_batch(testX)
    
    
    
    
    
    
    
    
    p_score_diff = round(predicted[0][0])
    p_score_offset = round(predicted[0][1])
    
    home_score = 0.0
    away_score = 0.0
    if p_score_diff > 0:
        home_score = p_score_diff + p_score_offset
        away_score = p_score_offset
    elif p_score_diff < 0:
        home_score = p_score_offset
        away_score = abs(p_score_diff) + p_score_offset
    else:
        home_score = p_score_offset
        away_score = p_score_offset
        
    return home_score, away_score

