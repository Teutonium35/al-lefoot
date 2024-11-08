import pandas as pd
import numpy as np
import json
import event_extraction
import matplotlib.pyplot as plt

def PPDA(id_equipe, id_match):
    match_event = event_extraction.get_events_from_match_id(id_match)

    nb_pass_ennemis = 0
    nb_action_def = 0

    for i in range (len(match_event)):
        action = match_event[i]['type']['name']
        if match_event[i]['team']['id'] != id_equipe:
            if action == 'Pass':
                if match_event[i][action.lower()]["end_location"][0] > 48 :
                    nb_pass_ennemis += 1
        else:
            if action == "Tackles" or action == "Foul Committed" or action == "Duel" or action == "Interception":
                if match_event[i]['location'][0] > 48:
                    nb_action_def += 1

    return nb_pass_ennemis/np.max((nb_action_def,1))

def afficher_data(teams, ppda):
    fig, ax = plt.subplots()
    ax.barh(teams, ppda)

    ax.set_ylabel('PPDA pour un match')
    ax.set_title('Résultats des différentes equipe de la competition sur les differents matchs')
    ax.legend(title='ppda')

    plt.show()

def compute_ppda(id_competition, id_season):
    match_list = event_extraction.get_matches_from_season_and_competition(id_competition, id_season)
    team, ppda = [], []
    for k in range (len(match_list)):
        try:
            match_event = event_extraction.get_events_from_match_id(match_list[k])
            team1 = match_event[1]["team"]["id"]
            team2 = match_event[1]["possession_team"]["id"]
            team.append(match_event[1]["team"]["name"])
            team.append(match_event[1]["possession_team"]["name"])
            ppda.append(PPDA(team1, match_list[k]))
            ppda.append(PPDA(team2, match_list[k]))

        except:
            print('error')
    return team, ppda

if __name__ == "__main__":

    team, ppda = compute_ppda(2,27)
    afficher_data(team, ppda)
    
    