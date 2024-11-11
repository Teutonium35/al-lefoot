import pandas as pd
import event_extraction
import json
import numpy as np
from catboost import CatBoostClassifier, CatBoostRegressor, Pool
import matplotlib.pyplot as plt

def getAction(match_event):
    team = match_event[0]["possession_team"]["id"]
    match_action_team1, match_action_team2, match_action = [], [], []

    for i in range(2,len(match_event)):
        if match_event[i]['team']['id'] == team:
            if match_event[i]['type']['name'] == 'Dribble' or match_event[i]['type']['name'] == 'Shot' or match_event[i]['type']['name'] == 'Carry' or match_event[i]['type']['name'] == 'Own Goal For' or match_event[i]['type']['name'] == 'Pass' or match_event[i]['type']['name'] == 'Own Goal Against':
                match_action_team1.append(match_event[i])
                match_action.append(match_event[i])
        else:
            if match_event[i]['type']['name'] == 'Dribble' or match_event[i]['type']['name'] == 'Shot' or match_event[i]['type']['name'] == 'Carry' or match_event[i]['type']['name'] == 'Own Goal For' or match_event[i]['type']['name'] == 'Pass' or match_event[i]['type']['name'] == 'Own Goal Against':
                match_action_team2.append(match_event[i])
                match_action.append(match_event[i])

    return match_action, match_action_team1, match_action_team2

def VAEP(proba):
    pS, pD = proba[:,0], proba[:,1]
    return (pS[1:]-pS[:-1]) - (pD[1:] - pD[:-1])


def traitement(match_event):
    match_action, match_action_team1, match_action_team2 = getAction(match_event)
    data, labels = extract_features(match_action)
    proba = ML(data,labels)
    vaep = VAEP(proba)
    print(pd.DataFrame(vaep))
    afficher_data(vaep[:50])

def afficher_data(data):
    fig, ax = plt.subplots()
    ax.barh([i for i in range (len(data))], data)

    ax.set_ylabel('VAEP')
    ax.set_title('VAEP des différentes actions')
    ax.legend(title='VAEP')

    plt.show()

def ML(data, labels):
    print(data)
    train_data, test_data = data[:1000], data[1000:]
    train_labels, test_labels = labels[:1000], labels[1000:]
    model = CatBoostClassifier(iterations=2,
                           depth=2,
                           learning_rate=1,
                           loss_function='Logloss',
                           verbose=True)
    # train the model
    model.fit(train_data, train_labels)
    # make the prediction using the resulting model
    preds_class = model.predict(test_data)
    preds_proba = model.predict_proba(test_data)
    return preds_proba

def extract_features(match_action):
    data = []
    labels = []
    colonnes = ['dx aᵢ', 'dx aᵢ₋₁ → aᵢ',  'dx  aᵢ₋₂ → aᵢ', 'dx aᵢ₋₁', 'dx  aᵢ₋₂', 'dy aᵢ', 'dy aᵢ₋₁ → aᵢ',  'dy  aᵢ₋₂ → aᵢ', 'dy aᵢ₋₁', 'dy  aᵢ₋₂', 'End location angle to goal aᵢ', 'End location angle to goal aᵢ₋₁', 'End location angle to goal aᵢ₋₂', 'End location dist to goal aᵢ', 'End location dist to goal aᵢ₋₁', 'End location dist to goal aᵢ₋₂', 'End location x aᵢ', 'End location x aᵢ₋₁', 'End location x aᵢ₋₂', 'End location y aᵢ', 'End location y aᵢ₋₁', 'End location y aᵢ₋₂',
    'Start location angle to goal aᵢ', 'Start location angle to goal aᵢ₋₁', 'Start location angle to goal aᵢ₋₂', 'Start location dist to goal aᵢ', 'Start location dist to goal aᵢ₋₁', 'Start location dist to goal aᵢ₋₂', 'Start location x aᵢ', 'Start location x aᵢ₋₁', 'Start location x aᵢ₋₂', 'Start location y aᵢ', 'Start location y aᵢ₋₁', 'Start location y aᵢ₋₂', 'Same team in possession aᵢ₋₁ → aᵢ', 'Same team in possession aᵢ₋₂ → aᵢ', 'Δtime aᵢ₋₁ aᵢ', 'Δtime aᵢ₋₂ aᵢ', 'Time elapsed in period aᵢ', 'Time elapsed in period aᵢ₋₁', 'Time elapsed in period aᵢ₋₂', 'Time elapsed in match aᵢ', 'Time elapsed in match aᵢ₋₁', 'Time elapsed in match aᵢ₋₂']

    start_localisationN_2 = match_action[0]["location"]
    start_localisationN_1 = match_action[1]["location"]

    action = match_action[0]["type"]["name"].lower()
    try :
        end_localisationN_2 = match_action[0][action]["end_location"]
    except :
        end_localisationN_2 = start_localisationN_2

    distN_2 = np.sqrt((end_localisationN_2[0] - 120)**2 + (end_localisationN_2[1] - 40)**2)
    anglN_2 = np.arccos((120 - end_localisationN_2[0])/distN_2)
    start_distN_2 = np.sqrt((start_localisationN_2[0] - 120)**2 + (start_localisationN_2[1] - 40)**2)
    start_anglN_2 = np.arccos((120 - start_localisationN_2[0])/start_distN_2)

    action = match_action[1]["type"]["name"].lower()
    try :
        end_localisationN_1 = match_action[1][action]["end_location"]
    except :
        end_localisationN_1 = start_localisationN_1

    distN_1 = np.sqrt((end_localisationN_1[0] - 120)**2 + (end_localisationN_1[1] - 40)**2)
    anglN_1 = np.arccos((120 - end_localisationN_1[0])/distN_1)
    start_distN_1 = np.sqrt((start_localisationN_1[0] - 120)**2 + (start_localisationN_1[1] - 40)**2)
    start_anglN_1 = np.arccos((120 - start_localisationN_1[0])/start_distN_1)


    for i in range (2,len(match_action)-1):
        start_localisationN = match_action[i]["location"]
        action = match_action[i]["type"]["name"].lower()
        try :
            end_localisationN = match_action[i][action]["end_location"]
        except :
            end_localisationN = start_localisationN

        distN = np.sqrt((end_localisationN[0] - 120)**2 + (end_localisationN[1] - 40)**2)
        anglN = np.arccos((120 - end_localisationN[0])/distN)
        start_distN = np.sqrt((start_localisationN[0] - 120)**2 + (start_localisationN[1] - 40)**2)
        start_anglN = np.arccos((120 - start_localisationN[0])/start_distN)

        #définition des features
        features = [end_localisationN[0] - start_localisationN[0], 
        start_localisationN[0] - end_localisationN_1[0], 
        start_localisationN[0] - end_localisationN_2[0], 
        end_localisationN_1[0] - start_localisationN_1[0], 
        end_localisationN_2[0] - start_localisationN_2[0], 
        end_localisationN[1] - start_localisationN[1], 
        start_localisationN[1] - end_localisationN_1[1], 
        start_localisationN[1] - end_localisationN_2[1], 
        end_localisationN_1[1] - start_localisationN_1[1], 
        end_localisationN_2[1] - start_localisationN_2[1],
        anglN, anglN_1, anglN_2,
        distN, distN_1, distN_2,
        end_localisationN[0], end_localisationN_1[0], end_localisationN_2[0],
        end_localisationN[1], end_localisationN_1[1], end_localisationN_2[1],
        start_anglN, start_anglN_1, start_anglN_2,
        start_distN, start_distN_1, start_distN_2,
        start_localisationN[0], start_localisationN_1[0], start_localisationN_2[0],
        start_localisationN[1], start_localisationN_1[1], start_localisationN_2[1],
        match_action[i]['possession_team']["id"] == match_action[i-1]['possession_team']["id"],
        match_action[i]['possession_team']["id"] == match_action[i-2]['possession_team']["id"],
        match_action[i-1]['minute']*60 + match_action[i-2]['second'] - match_action[i]['minute']*60 + match_action[i-1]['second'],
        match_action[i-2]['minute']*60 + match_action[i-1]['second'] - match_action[i]['minute']*60 + match_action[i]['second'],
        match_action[i]['minute']*60 + match_action[i]['second'],
        match_action[i-1]['minute']*60 + match_action[i-1]['second'],
        match_action[i-2]['minute']*60 + match_action[i-2]['second'],
        match_action[i]['minute']*60 + match_action[i]['second'] - (match_action[i]["period"]-1)*90*60,
        match_action[i-1]['minute']*60 + match_action[i-1]['second'] - (match_action[i-1]["period"]-1)*90*60,
        match_action[i-2]['minute']*60 + match_action[i-2]['second'] - (match_action[i-2]["period"]-1)*90*60]



        start_localisationN_2, start_localisationN_1 = start_localisationN_1, start_localisationN
        end_localisationN_2, end_localisationN_1 = end_localisationN_1, end_localisationN
        anglN_2, anglN_1 = anglN_1, anglN
        distN_2, distN_1 = distN_1, distN

        #définition des labels : savoir si l'action est un "succes ou non"
        try :
            res = (match_action[i][action]['outcome']["name"] == 'Complete')    #vaut True si la valeur est 'Complete' et False sinon (c'est à dire 'Incomplete)
        except :
            res = match_action[i]['possession_team']["id"] == match_action[i+1]['possession_team']["id"]
        labels.append(res)
        data.append(features)

    data = pd.DataFrame(data=data, columns=colonnes)
    labels = pd.DataFrame(data=labels, columns=['labels'])
    return data, labels

if __name__ == "__main__":
    path = "Innovation\open-data\data\competitions.json"

    # Lire le fichier JSON
    df = pd.read_json(path)
    print(df)
    
    # Afficher le DataFrame
    n = len(df)
    for i in range (1):
        try :
            data = event_extraction.get_matches_from_season_and_competition(df["competition_id"][i], df["season_id"][i])
        except :
            data = []
        
        data = event_extraction.get_matches_from_season_and_competition(2,27)
        m = len(data)
        m = 1
        for k in range (m):
            match_event = event_extraction.get_events_from_match_id(data[k])
            traitement(match_event)