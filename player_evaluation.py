from pathlib import Path
from json import loads
from event_extraction import get_events_from_match_id
from typing import List, Set, Tuple, Dict
from xt import get_positions_from_pass, get_field_indexes_from_coordinates, get_array_position_from_field_indexes, get_positions_from_carry



def load_matrix() -> List[int]:
    matrix_path = Path(__file__).parent / "result.json" 
    with open(matrix_path) as matrix_file:
        xt_matrix = loads(matrix_file.read())
    # print(xt_matrix)
    return xt_matrix

# def choose_target():

def scan_competitions() -> Set[str]:
    competitions_set = set()

    competitions_path = Path(__file__).parent.parent / 'open-data' / 'data' / 'competitions.json'
    with open(competitions_path) as competition_file:
        competitions_data = loads(competition_file.read())
    for competition in competitions_data:
        competitions_set.add(competition["competition_name"])

    print(competitions_set)

    return competitions_set

def choose_competition() -> str:
    competition_set = scan_competitions()

    user_dict = dict()

    index = 0
    for competition in competition_set:
        user_dict[index] = competition
        index += 1
        print(f"{index}. {competition}")
    
    chosen_index = input("Please input chosen competition\n>")
    chosen_competition = user_dict[int(chosen_index)-1]
    print(chosen_competition)
    # print(user_dict)

    return chosen_competition


def scan_seasons(competition_name: str) -> Set[str]:
    season_set = set()

    competition_path = Path(__file__).parent.parent / 'open-data' / 'data' / 'competitions.json'
    with open(competition_path) as competition_file:
        competition = loads(competition_file.read())
    for competition in competition:
        if competition["competition_name"] == competition_name:
            season_set.add(competition["season_name"])

    print(season_set)

    return season_set

def choose_season(competition_name: str) -> str:
    seasons_set = scan_seasons(competition_name)

    user_dict = dict()

    index = 0
    for season in seasons_set:
        user_dict[index] = season
        index += 1
        print(f"{index}. {season}")
    
    chosen_index = input("Please input chosen season\n>")
    chosen_season = user_dict[int(chosen_index)-1]
    print(chosen_season)

    return chosen_season

def scan_matches(competition_to_search: str, season_to_search: str) -> Tuple[str,str]:
    competition_path = Path(__file__).parent.parent / 'open-data' / 'data' / 'competitions.json'
    with open(competition_path) as competition_file:
        competitions = loads(competition_file.read())
    print(f'{competition_to_search=}')
    print(f'{season_to_search=}')
    for competition in competitions:
        print(f'{competition["competition_name"]=}')
        print(f'{competition=}')
        if competition["competition_name"] == competition_to_search and competition["season_name"] == season_to_search:
            print("found competition")
            competition_id = competition["competition_id"]
            season_id = competition["season_id"]
    season_path = Path(__file__).parent.parent / 'open-data' / 'data' / 'matches' / f'{competition_id}' / f'{season_id}.json'


    home_team_set = set()
    with open(season_path) as matches_file:
        matches = loads(matches_file.read())
        for match in matches:
            home_team_set.add(match["home_team"]["home_team_name"])

    
    user_dict = dict()

    index = 0
    for home_team in home_team_set:
        user_dict[index] = home_team
        index += 1
        print(f"{index}. {home_team}")
    
    chosen_index = input("Please input chosen home team\n>")
    chosen_home_team = user_dict[int(chosen_index)-1]
    print(chosen_home_team)




    away_team_set = set()
    with open(season_path) as matches_file:
        matches = loads(matches_file.read())
        print(f'{matches=}')
        for match in matches:
            if match["home_team"]["home_team_name"] == chosen_home_team:
                away_team_set.add(match["away_team"]["away_team_name"])
    print(f'{away_team_set=}')
    
    user_dict = dict()

    index = 0
    for away_team in away_team_set:
        user_dict[index] = away_team
        index += 1
        print(f"{index}. {away_team}")
    
    chosen_index = input("Please input chosen away team\n>")
    chosen_away_team = user_dict[int(chosen_index)-1]
    print(chosen_away_team)

    return chosen_home_team, chosen_away_team

def get_competition_id_from_name(competition_name: str) -> int:
    competition_path = Path(__file__).parent.parent / 'open-data' / 'data' / 'competitions.json'
    with open(competition_path) as competition_file:
        competitions = loads(competition_file.read())
    for competition in competitions:
        if competition["competition_name"] == competition_name:
            return competition["competition_id"]
    raise ValueError
        
def get_season_id_from_name(season_name: str) -> int:
    season_path = Path(__file__).parent.parent / 'open-data' / 'data' / 'competitions.json'
    with open(season_path) as season_file:
        seasons = loads(season_file.read())
    for season in seasons:
        if season["season_name"] == season_name:
            return season["season_id"]
    raise ValueError


def get_match(competition: str, season: str, home_team: str, away_team: str) -> Dict:
    competition_id = get_competition_id_from_name(competition)
    season_id = get_season_id_from_name(season)
    season_path = Path(__file__).parent.parent / 'open-data' / 'data' / 'matches' / f'{competition_id}' / f'{season_id}.json'


    with open(season_path) as matches_file:
        matches = loads(matches_file.read())
    for match in matches:
        if match["home_team"]["home_team_name"] == home_team and match["away_team"]["away_team_name"] == away_team:
            return match

def choose_player(match: Dict) -> str:
    lineup_path = Path(__file__).parent.parent / 'open-data' / 'data' / 'lineups' / f'{match["match_id"]}.json'
    with open(lineup_path) as lineup_file:
        lineup = loads(lineup_file.read())
        print(f'{lineup=}')
    players_set = set()
    for team in lineup:
        for player in team["lineup"]:
            players_set.add(player["player_name"])
    print(f'{players_set=}')


    user_dict = dict()

    index = 0
    for player in players_set:
        user_dict[index] = player
        index += 1
        print(f"{index}. {player}")
    
    chosen_index = input("Please input chosen away team\n>")
    chosen_player = user_dict[int(chosen_index)-1]
    print(chosen_player)

    return chosen_player

def get_player_events(match: Dict, player: str) -> Tuple[Set[Dict], Set[Dict]]:
    events = get_events_from_match_id(match["match_id"])
    print(f'{len(events)=}')


    sorted_events = list()
    for event in events:
        try:
            print(f'{event["player"]["name"]=}')
            print(f'{player=}')
            if event["player"]["name"] == player:
                print("ok here")
                sorted_events.append(event)
                # print(f'{sorted_events=}')

        except KeyError:
            pass
    # print(f'{sorted_events=}')


    pass_events = []
    carry_events = []
    successful_shot_events = []
    missed_shot_events = []

    total_length = len(sorted_events)
    current_index = 0
    for event in sorted_events:
        print(f'{event=}')
        current_index += 1
        print(f"Sorting events... {int(current_index/total_length*100)}%", end='\r')
        try:
            if event["type"]["name"] == "Pass":
                pass_events.append(event)
            elif event["type"]["name"] == "Carry":
                carry_events.append(event)
            elif event["type"]["name"] == "Shot":
                if event["shot"]["outcome"]["name"] == "Goal":
                    successful_shot_events.append(event)
                else:
                    missed_shot_events.append(event)
        except:
            print(f"Could not process event {event}")

    return pass_events, carry_events

def choose_subject() -> Tuple[str, str, str, str, str, str]:
    # xt_matrix = load_matrix()
    competition = choose_competition()
    season = choose_season(competition)
    home_team, away_team = scan_matches(competition, season)

    match = get_match(competition, season, home_team, away_team)

    player = choose_player(match)

    return competition, season, home_team, away_team, match, player

def rate_pass(pass_event: Dict) -> int:
    xt_matrix = load_matrix()
    start_x, start_y, end_x, end_y = get_positions_from_pass(pass_event)
    start_lindex, start_windex = get_field_indexes_from_coordinates(start_x, start_y)
    end_lindex, end_windex = get_field_indexes_from_coordinates(end_x, end_y)
    start_array_index = get_array_position_from_field_indexes(start_lindex, start_windex)
    end_array_index = get_array_position_from_field_indexes(end_lindex, end_windex)

    xt_score = xt_matrix[end_array_index] - xt_matrix[start_array_index]

    # print(f'{xt_matrix=}')
    # print(f'{xt_matrix[end_array_index]=}')
    # print(f'{xt_matrix[start_array_index]=}')
    return xt_score

def rate_carry(carry_event: Dict):
    xt_matrix = load_matrix()
    start_x, start_y, end_x, end_y = get_positions_from_carry(carry_event)
    start_lindex, start_windex = get_field_indexes_from_coordinates(start_x, start_y)
    end_lindex, end_windex = get_field_indexes_from_coordinates(end_x, end_y)
    start_array_index = get_array_position_from_field_indexes(start_lindex, start_windex)
    end_array_index = get_array_position_from_field_indexes(end_lindex, end_windex)

    xt_score = xt_matrix[end_array_index] - xt_matrix[start_array_index]

    # print(f'{xt_matrix=}')
    # print(f'{xt_matrix[end_array_index]=}')
    # print(f'{xt_matrix[start_array_index]=}')
    return xt_score


if __name__ == "__main__":
    # print(competition)
    # print(season)
    # competition, season, home_team, away_team, match, player = choose_subject()
    competition = "Ligue 1"
    season = "2015/2016"
    home_team = "Paris Saint-Germain"
    away_team = "Marseille"
    match = get_match(competition, season, home_team, away_team)
    player = "Marco Verratti"
    # player = "Zlatan Ibrahimović"

    pass_events, carry_events = get_player_events(match, player)
    # print(f'{pass_events=}')
    print(f'{len(pass_events)=}')
    total_score = 0
    for pass_event in pass_events:
        total_score += rate_pass(pass_event)
    for carry_event in carry_events:
        total_score += rate_carry(carry_event)
    print(f'{total_score=}')