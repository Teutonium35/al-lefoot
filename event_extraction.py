from pathlib import Path
from json import loads
from typing import List, Dict

competition_id = 7
season_id = 27
match_path = Path(__file__).parent / 'temp.json'

class Event:
    def __init__(self, raw_content: Dict):
        self.raw_content = raw_content
        

class Match:
    def __init__(self, match_id: int):
        self.match_id = match_id

    def get_events(self) -> List[Event]:
        events_path = Path(__file__).parent.parent / 'open-data' / 'data' / 'events' / f'{self.match_id}.json'

        with open(events_path) as events_file:
            events_data = loads(events_file.read())

        return [Event(event_details) for event_details in events_data]



def get_matches_from_season_and_competition(competition_id: int, season_id: int) -> List[Match]:
    match_path = Path(__file__).parent.parent / 'open-data' / 'data' / 'matches' / f'{competition_id}' / f'{season_id}.json'

    with open(match_path) as match_file:
        match_data = loads(match_file.read())

    return [Match(match_details['match_id']) for match_details in match_data]

def get_full_matches():
    full_matches_list = []
    root_dir = Path(__file__).parent.parent / 'open-data' / 'data' / 'matches'
    for dir in root_dir.iterdir():
        for file in dir.iterdir():
            with open(file) as match_file:
                match_data = loads(match_file.read())
            match_list = [Match(match_details['match_id']) for match_details in match_data]
            for match_data in match_list:
                full_matches_list.append(match_data)

    return full_matches_list













get_full_matches()
get_matches_from_season_and_competition(2,27)