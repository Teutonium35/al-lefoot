from pathlib import Path
from json import loads

competition_id = 7
season_id = 27

match_path = Path(__file__).parent.parent / 'open-data' / 'data' / 'matches' / f'{competition_id}' / f'{season_id}.json'

print(f'{match_path=}')

with open(match_path) as match_file:
    match_data = loads(match_file.read())

print(f'{match_data=}')