from pathlib import Path
from json import loads

competition_id = 7
season_id = 27
match_path = Path(__file__).parent / 'temp.json'


def get_matches_from_season_and_competition(competition_id: int, season_id: int):
    match_path = Path(__file__).parent.parent / 'open-data' / 'data' / 'matches' / f'{competition_id}' / f'{season_id}.json'

    # print(f'{match_path=}')

    with open(match_path) as match_file:
        match_data = loads(match_file.read())

    # print(f'{match_data=}')

    match_list = [match_details['match_id'] for match_details in match_data]

    # print(f'{match_list=}')
    return match_list

def get_events_from_match_id(match_id: int):
    events_path = Path(__file__).parent.parent / 'open-data' / 'data' / 'events' / f'{match_id}.json'

    with open(events_path) as events_file:
        events_data = loads(events_file.read())

    # events_id_list = [event_details['id'] for event_details in events_data]

    # print(f'{events_id_list=}')
    return events_data